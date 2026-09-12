"""
Speech-to-text via Groq's hosted Whisper API.

Why Groq Whisper: it is free (2,000 requests/day, 28,800 audio-seconds/day
on the free tier as of this writing), fast, and its language detection is
automatic - we never tell it what language to expect, so a Russian-language
bot interface never biases recognition of an English voice message, and
vice versa (spec section 5).

This module only knows how to turn audio bytes into text. Swapping the
STT provider later (e.g. for a different Groq model, or a different
vendor entirely) only means editing this file - nothing in the Telegram
handlers or in summarization.py needs to change.
"""

from __future__ import annotations

import logging

import groq

from app.config import settings
from app.services.errors import RateLimitReached, ServiceUnavailable, TranscriptionFailed

logger = logging.getLogger(__name__)

_client = groq.AsyncGroq(api_key=settings.groq_api_key, timeout=settings.request_timeout_seconds)


async def transcribe_voice(audio_bytes: bytes, filename: str = "voice.ogg") -> str:
    """
    Transcribe a single voice message.

    No `language` hint is passed to the API on purpose - Whisper's
    automatic language detection decides per voice message, independent
    of the bot's interface language.
    """
    try:
        result = await _client.audio.transcriptions.create(
            model=settings.stt_model,
            file=(filename, audio_bytes),
            response_format="json",
            temperature=0.0,
        )
    except groq.RateLimitError as exc:
        logger.warning("Groq STT rate limit reached")
        raise RateLimitReached("Speech-to-text rate limit reached") from exc
    except (groq.APIConnectionError, groq.APITimeoutError) as exc:
        logger.error("Groq STT unreachable: %s", exc)
        raise ServiceUnavailable("Speech-to-text service is unreachable") from exc
    except groq.APIStatusError as exc:
        logger.error("Groq STT API error, status=%s", exc.status_code)
        raise TranscriptionFailed(f"Speech-to-text failed with status {exc.status_code}") from exc

    return (result.text or "").strip()
