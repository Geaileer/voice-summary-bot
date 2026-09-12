"""
Ties together audio download, transcription and summarization for one
"Done" button press, and turns any failure into the right localized,
user-facing message. Full technical details always go to the logs -
never a stack trace to the user (spec section 17).
"""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.types import Message

from app.config import settings
from app.services.audio import download_voice
from app.services.errors import (
    DownloadFailed,
    FileTooLarge,
    ProcessingError,
    RateLimitReached,
    ServiceUnavailable,
    SummarizationFailed,
    TranscriptionFailed,
)
from app.services.summarization import summarize_transcript
from app.services.transcription import transcribe_voice
from app.utils.formatting import format_result_messages
from app.utils.retry import retry_once_on
from app.utils.texts import t

logger = logging.getLogger(__name__)

_ERROR_TEXT_KEYS: dict[type[Exception], str] = {
    FileTooLarge: "error_file_too_large",
    DownloadFailed: "error_download",
    RateLimitReached: "error_rate_limit",
    ServiceUnavailable: "error_service_unavailable",
    TranscriptionFailed: "error_transcription",
    SummarizationFailed: "error_summarization",
}


async def run_pipeline(
    bot: Bot,
    chat_id: int,
    lang: str,
    voices: list[dict],
    status_message: Message,
) -> None:
    """Process one batch of voice messages and send the result to `chat_id`."""
    logger.info("chat=%s: starting processing of %d voice message(s)", chat_id, len(voices))
    transcripts: list[str] = []

    try:
        for index, voice in enumerate(voices, start=1):
            logger.info("chat=%s: downloading voice %d/%d", chat_id, index, len(voices))
            audio_bytes = await download_voice(bot, voice["file_id"])

            logger.info("chat=%s: transcribing voice %d/%d", chat_id, index, len(voices))
            text = await retry_once_on(
                RateLimitReached,
                settings.rate_limit_retry_delay_seconds,
                lambda ab=audio_bytes, i=index: transcribe_voice(ab, filename=f"voice_{i}.ogg"),
            )
            del audio_bytes  # never kept around longer than needed

            if text:
                transcripts.append(text)

        if not transcripts:
            logger.info("chat=%s: no speech recognized in any voice message", chat_id)
            await status_message.edit_text(t(lang, "error_no_speech"))
            return

        full_transcript = "\n\n".join(transcripts)
        logger.info("chat=%s: summarizing transcript (%d chars)", chat_id, len(full_transcript))

        summary, key_points = await retry_once_on(
            RateLimitReached,
            settings.rate_limit_retry_delay_seconds,
            lambda: summarize_transcript(full_transcript),
        )

        logger.info("chat=%s: processing finished successfully", chat_id)
        await status_message.delete()

        for chunk in format_result_messages(lang, summary, key_points, full_transcript):
            await bot.send_message(chat_id, chunk)

    except ProcessingError as exc:
        text_key = _ERROR_TEXT_KEYS.get(type(exc), "error_generic")
        logger.error("chat=%s: processing failed (%s): %s", chat_id, type(exc).__name__, exc)
        await status_message.edit_text(t(lang, text_key))
    except Exception:
        logger.exception("chat=%s: unexpected error during processing", chat_id)
        await status_message.edit_text(t(lang, "error_generic"))
    finally:
        transcripts.clear()
