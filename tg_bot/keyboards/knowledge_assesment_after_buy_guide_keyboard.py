__all__ = ["get_knowledge_assesment_after_buy_guide_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.filters.callback_data import (AfterBuyKnowledgeAssesmentPageCallbackData,
                                          SecondAfterBuyKnowledgeAssesmentGuidePageCallbackData)

def get_knowledge_assesment_after_buy_guide_keyboard(callback_data: AfterBuyKnowledgeAssesmentPageCallbackData |
                     SecondAfterBuyKnowledgeAssesmentGuidePageCallbackData) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=callback_data().pack()
        )
    )
    return keyboard.as_markup()
