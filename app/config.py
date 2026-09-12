"""
Application configuration.

All settings are read from environment variables (via a local .env file
during development, or real environment variables in production/Railway).
Nothing secret ever lives in source code - see .env.example for the
list of variables you need to set.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    groq_api_key: str

    # Groq model IDs. Kept configurable so the AI provider/model can be
    # swapped later (e.g. a newer Groq model) without touching any other
    # part of the codebase - see app/services/transcription.py and
    # app/services/summarization.py.
    stt_model: str
    summary_model: str

    # Product limits described in the spec.
    max_voices_per_session: int
    max_voice_file_size_mb: int

    # Network/service behaviour.
    request_timeout_seconds: int
    rate_limit_retry_delay_seconds: float


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer, got: {raw!r}") from exc


def _get_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be a number, got: {raw!r}") from exc


def load_settings() -> Settings:
    bot_token = (os.getenv("BOT_TOKEN") or "").strip()
    groq_api_key = (os.getenv("GROQ_API_KEY") or "").strip()

    if not bot_token:
        raise RuntimeError(
            "BOT_TOKEN is not set. Copy .env.example to .env and fill in your "
            "Telegram bot token from @BotFather."
        )
    if not groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and fill in "
            "your free API key from https://console.groq.com/keys"
        )

    return Settings(
        bot_token=bot_token,
        groq_api_key=groq_api_key,
        stt_model=os.getenv("STT_MODEL", "whisper-large-v3-turbo"),
        summary_model=os.getenv("SUMMARY_MODEL", "llama-3.3-70b-versatile"),
        max_voices_per_session=_get_int("MAX_VOICES_PER_SESSION", 10),
        max_voice_file_size_mb=_get_int("MAX_VOICE_FILE_SIZE_MB", 20),
        request_timeout_seconds=_get_int("REQUEST_TIMEOUT_SECONDS", 120),
        rate_limit_retry_delay_seconds=_get_float("RATE_LIMIT_RETRY_DELAY_SECONDS", 5.0),
    )


settings = load_settings()
