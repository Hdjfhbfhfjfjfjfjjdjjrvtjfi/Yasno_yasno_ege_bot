__all__ = ["get_user_profile_page_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from tg_bot.filters.callback_data import MainMenuPageCallbackData


def get_user_profile_page_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data=MainMenuPageCallbackData().pack()
        )
    )
    return keyboard.as_markup()