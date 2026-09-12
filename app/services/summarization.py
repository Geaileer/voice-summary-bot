"""
Summary + key points generation via Groq's free chat completion API.

Why Groq for this too: one free API key covers both speech-to-text and
the LLM step, which keeps setup (and the .env file) simple, and Groq's
free tier for llama-3.3-70b-versatile is generous enough for an MVP
(1,000 requests/day, 100,000 tokens/day as of this writing).

The model is asked to reply with a JSON object only (`response_format`
json_object) so the Telegram-facing code never has to parse loose,
unpredictable text - see the schema described in the system prompt below.

As with transcription.py, this file is the only place that knows which
LLM provider/model is used, so it can be swapped later without touching
the Telegram handlers.
"""

from __future__ import annotations

import json
import logging

import groq

from app.config import settings
from app.services.errors import RateLimitReached, ServiceUnavailable, SummarizationFailed

logger = logging.getLogger(__name__)

_client = groq.AsyncGroq(api_key=settings.groq_api_key, timeout=settings.request_timeout_seconds)

_SYSTEM_PROMPT = """\
You are an assistant that turns transcribed voice messages into a short, useful summary.

You will receive the full transcript of one or more voice messages, already \
concatenated in the exact order they were recorded.

Your job:
1. Understand the overall context across all the voice messages, respecting their order.
2. Write a short summary (2-4 sentences) that captures the actual substance - not a \
generic restatement of "the speaker talked about...".
3. Extract key points as short, standalone items: decisions, tasks, dates, names, \
agreements and important facts, if present in the transcript.
4. Never invent information that is not present in the transcript.
5. Do not simply restate each voice message one by one - genuinely synthesize the meaning.
6. Do not repeat obvious/trivial statements as key points.
7. Write the summary and key points in the same language as the transcript. If the \
transcript mixes languages, use whichever language dominates, and keep names/terms as spoken.
8. If the transcript contains no real content (e.g. silence, noise, a couple of filler \
words), say so plainly in the summary and return an empty key_points list.

Respond with ONLY a JSON object, no extra commentary before or after it, matching \
exactly this shape:
{"summary": "string", "key_points": ["string", "string"]}
"""


async def summarize_transcript(transcript: str) -> tuple[str, list[str]]:
    """Return (summary, key_points) for the given transcript text."""
    try:
        response = await _client.chat.completions.create(
            model=settings.summary_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": transcript},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
    except groq.RateLimitError as exc:
        logger.warning("Groq LLM rate limit reached")
        raise RateLimitReached("Summarization rate limit reached") from exc
    except (groq.APIConnectionError, groq.APITimeoutError) as exc:
        logger.error("Groq LLM unreachable: %s", exc)
        raise ServiceUnavailable("Summarization service is unreachable") from exc
    except groq.APIStatusError as exc:
        logger.error("Groq LLM API error, status=%s", exc.status_code)
        raise SummarizationFailed(f"Summarization failed with status {exc.status_code}") from exc

    raw_content = response.choices[0].message.content or "{}"
    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        logger.error("Could not parse summarization output as JSON")
        raise SummarizationFailed("Model returned output that was not valid JSON") from exc

    summary = str(data.get("summary", "")).strip()
    key_points_raw = data.get("key_points", [])
    if not isinstance(key_points_raw, list):
        key_points_raw = []
    key_points = [str(item).strip() for item in key_points_raw if str(item).strip()]

    if not summary:
        raise SummarizationFailed("Model returned an empty summary")

    return summary, key_points
