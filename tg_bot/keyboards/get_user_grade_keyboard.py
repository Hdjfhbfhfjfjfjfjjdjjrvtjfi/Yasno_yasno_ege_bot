__all__ = ["get_get_user_grade_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from tg_bot.filters.callback_data import GetUserGradeCallbackData


def get_get_user_grade_keyboard(grades: tuple[int, ...]) -> InlineKeyboardMarkup:
    """Creates a keyboard for selecting user's grade/class level.
    
    The keyboard includes:
    - A list of grade options as numbered buttons
    - Each button contains the grade number and is linked to the corresponding grade selection

    :param grades: Tuple of available grade numbers
    :return: InlineKeyboardMarkup with grade selection options
    """
    keyboard = InlineKeyboardBuilder()
    for i, grade in enumerate(grades):
        keyboard.row(
            InlineKeyboardButton(
                text=str(grade),
                callback_data=GetUserGradeCallbackData(grade=grade).pack()
            )
        )
    return keyboard.as_markup()