from __future__ import annotations
__all__ = ["get_choose_event_date_page_keyboard"]
from datetime import datetime

from locale import setlocale, LC_ALL

from typing import TYPE_CHECKING

from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.filters.callback_data import EventPageCallbackData, EventQuestionPageCallbackData, \
    MainMenuPageCallbackData, ChooseEventDatePageSwitchKeyboardCallbackData
from tg_bot.utils.validators import page_index_validator
if TYPE_CHECKING:
    from tg_bot.utils.enums import EventEnum

def get_choose_event_date_page_keyboard(events: tuple[tuple[UUID, datetime, bool], ...], cluster_index: int,
                                        count_of_clusters, event_type: EventEnum) -> InlineKeyboardMarkup:
    """Creates a keyboard for selecting event dates with pagination and navigation options.
    
    The keyboard includes:
    - A list of event dates with their availability status
    - Navigation buttons for moving between clusters
    - A button to return to the main menu

    :param events: Tuple of event tuples containing (UUID, datetime, availability status)
    :param cluster_index: Current cluster index for pagination
    :param count_of_clusters: Total number of clusters available
    :param event_type: Type of the event (excursion or knowledge assessment)
    :return: InlineKeyboardMarkup with date selection and navigation options
    """
    setlocale(LC_ALL, "Russian")
    keyboard = InlineKeyboardBuilder()
    for event in events:
        callback_data: CallbackData
        if event[2]:
            callback_data = EventPageCallbackData(id=str(event[0]), page_index=cluster_index, event=event_type)
        else:
            callback_data = EventQuestionPageCallbackData(page_index=cluster_index, event=event_type)
        keyboard.row(
            InlineKeyboardButton(
                text=event[1].strftime("%d %B %H:%M"),
                callback_data=callback_data.pack()
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ChooseEventDatePageSwitchKeyboardCallbackData(
                event=event_type,
                page_index=page_index_validator(cluster_index - 1, count_of_clusters - 1)
            ).pack()
        ),
        InlineKeyboardButton(
            text="Дальше",
            callback_data=ChooseEventDatePageSwitchKeyboardCallbackData(
                event=event_type,
                page_index=page_index_validator(cluster_index + 1, count_of_clusters - 1)
            ).pack()
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data=MainMenuPageCallbackData().pack()
        )
    )
    return keyboard.as_markup()