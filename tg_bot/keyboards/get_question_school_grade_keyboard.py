__all__ = ["get_get_question_school_grade_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.filters.callback_data import QuestionSchoolGradeCallbackData


def get_get_question_school_grade_keyboard(grades: tuple[int, ...]) -> InlineKeyboardMarkup:
    """Creates a keyboard for selecting school grade for questions.
    
    The keyboard includes:
    - A list of grade options as numbered buttons
    - Each button contains the grade number and is linked to the corresponding grade selection

    :param grades: Tuple of available grade numbers
    :return: InlineKeyboardMarkup with grade selection options
    """
    keyboard = InlineKeyboardBuilder()
    for grade in grades:
        keyboard.row(
            InlineKeyboardButton(
                text=f"{grade}",
                callback_data=QuestionSchoolGradeCallbackData(grade=grade).pack()
            )
        )
    return keyboard.as_markup()