"""
A deliberately small retry helper.

The free Groq tier can return a rate-limit error under normal use (e.g.
several people using the bot at once). Rather than failing immediately,
each Groq call gets exactly one retry after a short delay. If it still
fails, the caller's normal error handling takes over and the user gets a
clear "please try again later" message (see app/services/pipeline.py) -
this is not a generic backoff/queueing system, on purpose, to keep the
MVP simple.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Awaitable, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def retry_once_on(
    exception_type: type[Exception],
    delay_seconds: float,
    func: Callable[[], Awaitable[T]],
) -> T:
    """Call `func()`; on `exception_type`, wait and try exactly once more."""
    try:
        return await func()
    except exception_type:
        logger.warning("Retrying once after %s in %.1fs", exception_type.__name__, delay_seconds)
        await asyncio.sleep(delay_seconds)
        return await func()
