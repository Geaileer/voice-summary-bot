import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import settings
from app.keyboards.keyboards import done_keyboard
from app.states import BotStates
from app.utils.texts import t

router = Router(name="voice")
logger = logging.getLogger(__name__)


@router.message(BotStates.collecting_voices, F.voice)
async def on_voice_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang", "en")
    voices: list[dict] = data.get("voices", [])

    if len(voices) >= settings.max_voices_per_session:
        await message.answer(t(lang, "max_voices_error", max=settings.max_voices_per_session))
        return

    voice = message.voice
    max_bytes = settings.max_voice_file_size_mb * 1024 * 1024
    if voice.file_size and voice.file_size > max_bytes:
        await message.answer(t(lang, "error_file_too_large"))
        return

    voices.append({"file_id": voice.file_id, "duration": voice.duration})
    await state.update_data(voices=voices)

    count = len(voices)
    logger.info("chat=%s: received voice %d/%d", message.chat.id, count, settings.max_voices_per_session)

    await message.answer(
        t(lang, "received_count", count=count, max=settings.max_voices_per_session),
        reply_markup=done_keyboard(lang),
    )


@router.message(BotStates.processing)
async def on_message_during_processing(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang", "en")
    await message.answer(t(lang, "still_processing"))


@router.message(BotStates.collecting_voices)
async def on_non_voice_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang", "en")
    await message.answer(t(lang, "expected_voice"))


@router.message(BotStates.choosing_language)
async def on_message_before_language(message: Message) -> None:
    await message.answer(t("en", "before_language") + "\n" + t("ru", "before_language"))


@router.message()
async def on_message_no_state(message: Message) -> None:
    await message.answer(t("en", "no_active_session") + " / " + t("ru", "no_active_session"))
