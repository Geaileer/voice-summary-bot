from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.keyboards import language_keyboard
from app.states import BotStates

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(BotStates.choosing_language)
    await message.answer(
        "🌐 Choose your interface language / Выберите язык интерфейса:",
        reply_markup=language_keyboard(),
    )
