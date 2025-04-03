__all__ = ["get_get_user_grade_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from tg_bot.filters.callback_data import GetUserGradeCallbackData


def get_get_user_grade_keyboard(grades: tuple[int, ...]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for i, grade in enumerate(grades):
        keyboard.row(
            InlineKeyboardButton(
                text=str(grade),
                callback_data=GetUserGradeCallbackData(grade=grade).pack()
            )
        )
    return keyboard.as_markup()