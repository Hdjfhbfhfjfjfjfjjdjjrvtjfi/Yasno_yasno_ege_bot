__all__ = ["get_main_menu_page_keyboard"]
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tg_bot.filters.callback_data import ChooseEventDatePageCallbackData, UserProfilePageCallbackData
from tg_bot.utils.enums import EventEnum

def get_main_menu_page_keyboard(connection_link: str, has_excursion: bool, has_knowledge_assesment: bool) -> InlineKeyboardMarkup:
    """Creates the main menu keyboard with dynamic options based on user's current activities.
    
    The keyboard includes buttons for:
    - Signing up for an excursion (if not already signed up)
    - Taking a knowledge assessment (if not already taken)
    - Getting answers to questions (via external link)
    - Accessing user profile

    :param connection_link: URL for getting answers to questions
    :param has_excursion: Boolean indicating if user is already signed up for an excursion
    :param has_knowledge_assesment: Boolean indicating if user has already taken the knowledge assessment
    :return: InlineKeyboardMarkup with main menu options
    """
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
