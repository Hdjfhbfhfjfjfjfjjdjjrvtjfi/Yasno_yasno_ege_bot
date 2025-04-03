from __future__ import annotations
__all__ = ["get_event_question_page_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from typing import TYPE_CHECKING

from tg_bot.filters.callback_data import ChooseEventDatePageCallbackData
if TYPE_CHECKING:
    from tg_bot.utils.enums import EventEnum


def get_event_question_page_keyboard(connection_link: str, cluster_index: int, event_type: EventEnum) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Задать вопрос",
            url=connection_link,
            callback_data=None
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ChooseEventDatePageCallbackData(
                page_index=cluster_index,
                event=event_type
            ).pack()
        )
    )
    return keyboard.as_markup()