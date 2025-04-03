__all__ = ["agreement_on_data_processing_page_keyboard"]
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tg_bot.filters.callback_data import GetUserDataPageCallbackData

def agreement_on_data_processing_page_keyboard(agreement_on_data_processing_link: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Соглашение наобработку данных",
            url=agreement_on_data_processing_link,
            callback_data=None
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Согласен",
            callback_data=GetUserDataPageCallbackData().pack()
        )
    )
    return keyboard.as_markup()
