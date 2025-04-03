__all__ = ["get_get_question_school_grade_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.filters.callback_data import QuestionSchoolGradeCallbackData


def get_get_question_school_grade_keyboard(grades: tuple[int, ...]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for grade in grades:
        keyboard.row(
            InlineKeyboardButton(
                text=f"{grade}",
                callback_data=QuestionSchoolGradeCallbackData(grade=grade).pack()
            )
        )
    return keyboard.as_markup()