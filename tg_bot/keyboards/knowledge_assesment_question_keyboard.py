__all__ = ["get_knowledge_assesment_question_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.filters.callback_data import GetResponseToQuestionCallbackData

def get_knowledge_assesment_question_keyboard(answers: tuple[tuple[str, str], ...]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for answer_id, description in answers:
        keyboard.row(
            InlineKeyboardButton(
                text=description,
                callback_data=GetResponseToQuestionCallbackData(answer_id=answer_id).pack()
            )
        )
    return keyboard.as_markup()
