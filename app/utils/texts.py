"""
Interface text strings (Russian / English).

IMPORTANT: this only controls the bot's UI language. It has no effect on
which language the spoken voice messages are recognized in - speech
recognition auto-detects the language of each voice message independently
(see app/services/transcription.py).
"""

from __future__ import annotations

_TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        "language_set": "Язык интерфейса: 🇷🇺 Русский",
        "send_voices_prompt": (
            "Отправьте от 1 до {max} голосовых сообщений (до ~10 минут каждое).\n"
            "Когда закончите — нажмите «Готово»."
        ),
        "received_count": "Получено: {count}/{max}",
        "done_button": "✅ Готово",
        "no_voices_error": "Сначала отправьте хотя бы одно голосовое сообщение.",
        "max_voices_error": (
            "Достигнут лимит — максимум {max} голосовых сообщений за один раз.\n"
            "Нажмите «Готово», чтобы обработать уже отправленные."
        ),
        "expected_voice": "Пожалуйста, отправьте голосовое сообщение 🎤 или нажмите «Готово», когда закончите.",
        "before_language": "Пожалуйста, выберите язык интерфейса, нажав на одну из кнопок выше ⬆️",
        "no_active_session": "Отправьте /start, чтобы начать.",
        "still_processing": "⏳ Уже обрабатываю ваши голосовые сообщения — подождите немного.",
        "processing": "⏳ Обрабатываю голосовые сообщения... Это может занять немного времени.",
        "error_generic": "😕 Произошла непредвиденная ошибка при обработке. Попробуйте ещё раз.",
        "error_download": "Не удалось загрузить одно из голосовых сообщений из Telegram. Попробуйте ещё раз.",
        "error_file_too_large": (
            "Одно из голосовых сообщений превышает лимит Telegram для ботов (20 МБ).\n"
            "Попробуйте отправить более короткую запись."
        ),
        "error_rate_limit": (
            "Бесплатный лимит сервиса распознавания или анализа речи временно исчерпан.\n"
            "Попробуйте повторить через несколько минут."
        ),
        "error_service_unavailable": "Сервис распознавания или анализа речи временно недоступен. Попробуйте позже.",
        "error_transcription": "Не удалось распознать речь в голосовых сообщениях. Попробуйте записать их заново.",
        "error_summarization": "Не удалось составить краткое содержание. Попробуйте ещё раз, нажав «Готово».",
        "error_no_speech": "Не удалось распознать речь ни в одном из голосовых сообщений. Попробуйте отправить их заново.",
        "result_summary_header": "🧠 Кратко",
        "result_keypoints_header": "🔑 Главное",
        "result_transcript_header": "📝 Транскрипция",
    },
    "en": {
        "language_set": "Interface language: 🇬🇧 English",
        "send_voices_prompt": (
            "Send 1 to {max} voice messages (up to ~10 minutes each).\n"
            "When you're done, tap \u201cDone\u201d."
        ),
        "received_count": "Received: {count}/{max}",
        "done_button": "✅ Done",
        "no_voices_error": "Send at least one voice message first.",
        "max_voices_error": (
            "Limit reached - {max} voice messages max per session.\n"
            "Tap \u201cDone\u201d to process what you've already sent."
        ),
        "expected_voice": "Please send a voice message 🎤 or tap \u201cDone\u201d when you're finished.",
        "before_language": "Please choose your interface language using one of the buttons above ⬆️",
        "no_active_session": "Send /start to begin.",
        "still_processing": "⏳ Still processing your voice messages - please wait a moment.",
        "processing": "⏳ Processing your voice messages... this may take a little while.",
        "error_generic": "😕 An unexpected error occurred while processing. Please try again.",
        "error_download": "Couldn't download one of the voice messages from Telegram. Please try again.",
        "error_file_too_large": (
            "One of the voice messages exceeds Telegram's 20 MB bot download limit.\n"
            "Please try a shorter recording."
        ),
        "error_rate_limit": (
            "The free speech-recognition/analysis tier is temporarily rate-limited.\n"
            "Please try again in a few minutes."
        ),
        "error_service_unavailable": "The speech recognition or analysis service is temporarily unavailable. Please try again later.",
        "error_transcription": "Couldn't recognize speech in the voice messages. Please try recording them again.",
        "error_summarization": "Couldn't generate a summary. Please try again by tapping \u201cDone\u201d.",
        "error_no_speech": "No speech could be recognized in any of the voice messages. Please try sending them again.",
        "result_summary_header": "🧠 Summary",
        "result_keypoints_header": "🔑 Key points",
        "result_transcript_header": "📝 Transcript",
    },
}

_DEFAULT_LANG = "en"


def t(lang: str | None, key: str, **kwargs: object) -> str:
    """Look up a text string for the given interface language and fill placeholders."""
    lang_dict = _TEXTS.get(lang or "", _TEXTS[_DEFAULT_LANG])
    template = lang_dict.get(key) or _TEXTS[_DEFAULT_LANG].get(key, key)
    return template.format(**kwargs) if kwargs else template
