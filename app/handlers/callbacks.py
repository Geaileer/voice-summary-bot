import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.config import settings
from app.services.pipeline import run_pipeline
from app.states import BotStates
from app.utils.cleanup import clear_voice_session
from app.utils.texts import t

router = Router(name="callbacks")
logger = logging.getLogger(__name__)


@router.callback_query(BotStates.choosing_language, F.data.startswith("lang:"))
async def on_language_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.split(":", 1)[1]
    await state.update_data(lang=lang, voices=[])
    await state.set_state(BotStates.collecting_voices)

    await callback.message.edit_text(t(lang, "language_set"))
    await callback.message.answer(t(lang, "send_voices_prompt", max=settings.max_voices_per_session))
    await callback.answer()


@router.callback_query(BotStates.collecting_voices, F.data == "voices:done")
async def on_done_pressed(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    lang = data.get("lang", "en")
    voices: list[dict] = data.get("voices", [])

    if not voices:
        await callback.answer(t(lang, "no_voices_error"), show_alert=True)
        return

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    status_message = await callback.message.answer(t(lang, "processing"))

    await state.set_state(BotStates.processing)

    await run_pipeline(
        bot=bot,
        chat_id=callback.message.chat.id,
        lang=lang,
        voices=voices,
        status_message=status_message,
    )

    await clear_voice_session(state)
    await state.set_state(BotStates.collecting_voices)


@router.callback_query(BotStates.processing)
async def on_callback_during_processing(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang", "en")
    await callback.answer(t(lang, "still_processing"), show_alert=False)
