__all__ = ["get_event_after_buy_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from tg_bot.filters.callback_data import MainMenuPageCallbackData


def get_event_after_buy_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=MainMenuPageCallbackData().pack()
        )
    )
    return keyboard.as_markup()