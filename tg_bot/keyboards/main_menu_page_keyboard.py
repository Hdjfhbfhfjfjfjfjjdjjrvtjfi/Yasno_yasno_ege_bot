__all__ = ["get_main_menu_page_keyboard"]
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tg_bot.filters.callback_data import ChooseEventDatePageCallbackData, UserProfilePageCallbackData
from tg_bot.utils.enums import EventEnum

def get_main_menu_page_keyboard(connection_link: str, has_excursion: bool, has_knowledge_assesment: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if not has_excursion:
        keyboard.row(
            InlineKeyboardButton(
                text="Записаться на экскурсию \"Русский язык на вятке\"",
                callback_data=ChooseEventDatePageCallbackData(event=EventEnum.excursion).pack()
            )
        )
    if not has_knowledge_assesment:
        keyboard.row(
            InlineKeyboardButton(
                text="Оценить уровень знаний",
                callback_data=ChooseEventDatePageCallbackData(event=EventEnum.knowledge_assesment).pack()
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text="Получить ответ на вопрос",
            url=connection_link
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Профиль",
            callback_data=UserProfilePageCallbackData().pack()
        )
    )
    return keyboard.as_markup()
