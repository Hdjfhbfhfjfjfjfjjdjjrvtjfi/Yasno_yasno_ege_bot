from aiogram.handlers import CallbackQueryHandler
from aiogram.filters.callback_data import CallbackData

from typing import Type, Optional, Any, TypeVar, Generic

from tg_bot.models import Order, User, Excursion, KnowledgeAssesment
from tg_bot.services import PaymentService
from tg_bot.utils.enums import EventEnum
from tg_bot.utils.interfaces import IEvent
from tg_bot.utils.mixins import ConfigMixin, UnpackedCallbackDataMixin

T = TypeVar('T', bound=CallbackData)

class BaseEventHandler(Generic[T], CallbackQueryHandler, ConfigMixin, UnpackedCallbackDataMixin[T]):
    """Base class for event-related handlers."""

    async def handle(self) -> Any:
        raise NotImplementedError

    @property
    def event_model(self) -> Type[IEvent]:
        """Get the appropriate event model based on event type."""
        return Excursion if self.unpacked_callback_data.event == EventEnum.excursion else KnowledgeAssesment

    async def get_user(self) -> User:
        """Get the current user."""
        return await User.get_user_by_id(self.message.chat.id)

    @staticmethod
    async def get_user_order(user: User) -> Optional[Order]:
        """Get user's order and check if payment is successful."""
        order = await user.get_order()
        if order and PaymentService.get_payment_by_id(order.order_yookassa_id).is_succeed:
            return order
        return None