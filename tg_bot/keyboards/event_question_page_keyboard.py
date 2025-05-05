from __future__ import annotations
__all__ = ["get_event_question_page_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from typing import TYPE_CHECKING

from tg_bot.filters.callback_data import ChooseEventDatePageCallbackData
if TYPE_CHECKING:
    from tg_bot.utils.enums import EventEnum


def get_event_question_page_keyboard(connection_link: str, cluster_index: int, event_type: EventEnum) -> InlineKeyboardMarkup:
    """Creates a keyboard for the event question page with question submission and navigation options.
    
    The keyboard includes buttons for:
    - Submitting a question (via external link)
    - Returning to the event date selection page

    :param connection_link: URL for submitting questions
    :param cluster_index: Index of the current cluster in the date selection
    :param event_type: Type of the event (excursion or knowledge assessment)
    :return: InlineKeyboardMarkup with question submission and navigation options
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ChooseEventDatePageCallbackData(
                page_index=cluster_index,
                event=event_type
            ).pack()
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Задать вопрос",
            url=connection_link,
            callback_data=None
        )
    )
    return keyboard.as_markup()