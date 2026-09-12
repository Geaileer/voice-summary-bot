"""
Entry point.

Run with:  python -m app.bot
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent

from app.config import settings
from app.handlers import callbacks, start, voice

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # No default parse_mode: transcripts and LLM-generated summaries are
    # unpredictable free-form text that may contain "<", ">" or "&", which
    # would break Telegram's HTML/Markdown entity parser. Everything is
    # sent as plain text on purpose - simple and impossible to break.
    bot = Bot(token=settings.bot_token)
    # No database: user sessions (chosen language, collected voice file_ids)
    # live only in memory for the lifetime of the process - see spec section 9.
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(callbacks.router)
    dp.include_router(voice.router)

    @dp.errors()
    async def on_unhandled_error(event: ErrorEvent) -> bool:
        # Safety net so one bad update never crashes the whole bot, and so
        # nothing but a generic, logged error ever reaches this point -
        # every expected failure is already handled inside the pipeline.
        logger.exception("Unhandled exception while processing an update", exc_info=event.exception)
        return True

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started, polling for updates...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
