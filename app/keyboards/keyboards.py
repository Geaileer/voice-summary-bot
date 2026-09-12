from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.texts import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        ]
    )


def done_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "done_button"), callback_data="voices:done")],
        ]
    )
