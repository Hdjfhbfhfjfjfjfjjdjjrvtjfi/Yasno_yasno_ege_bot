from __future__ import annotations
__all__ = ["get_event_pay_page_keyboard"]
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from typing import TYPE_CHECKING

from tg_bot.filters.callback_data import EventCheckPaymentPageCallbackData, ChooseEventDatePageCallbackData
if TYPE_CHECKING:
    from tg_bot.utils.enums import EventEnum


def get_event_pay_page_keyboard(payment_link: str, cluster_index: int, event_type: EventEnum) -> InlineKeyboardMarkup:
    """Creates a keyboard for event payment page with payment and navigation options.
    
    The keyboard includes buttons for:
    - Checking payment status
    - Making payment (via external link)
    - Returning to the event date selection page

    :param payment_link: URL for making the payment
    :param cluster_index: Index of the current cluster in the date selection
    :param event_type: Type of the event (excursion or knowledge assessment)
    :return: InlineKeyboardMarkup with payment and navigation options
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Проверить оплату",
            callback_data=EventCheckPaymentPageCallbackData(event=event_type).pack()
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Оплатить",
            url=payment_link,
            callback_data=None
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ChooseEventDatePageCallbackData(page_index=cluster_index, event=event_type).pack()
        )
    )
    return keyboard.as_markup()