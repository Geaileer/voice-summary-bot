"""
Downloading voice messages from Telegram.

Design choice: voice files are downloaded straight into memory
(a BytesIO buffer) and handed to the transcription service immediately.
Nothing is ever written to disk, so there are no temporary audio files
to clean up afterwards - even if the bot crashes mid-request. This also
avoids relying on a writable filesystem, which some hosting setups
provide only ephemerally.
"""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramEntityTooLarge, TelegramNetworkError

from app.services.errors import DownloadFailed, FileTooLarge

logger = logging.getLogger(__name__)


async def download_voice(bot: Bot, file_id: str) -> bytes:
    """Download a single voice message and return its raw audio bytes."""
    try:
        buffer = await bot.download(file_id)
    except TelegramEntityTooLarge as exc:
        raise FileTooLarge("Voice message exceeds Telegram's 20 MB bot download limit") from exc
    except (TelegramBadRequest, TelegramNetworkError) as exc:
        logger.error("Failed to download voice message: %s", exc)
        raise DownloadFailed("Could not download voice message from Telegram") from exc

    if buffer is None:
        raise DownloadFailed("Telegram returned an empty file")

    return buffer.read()
