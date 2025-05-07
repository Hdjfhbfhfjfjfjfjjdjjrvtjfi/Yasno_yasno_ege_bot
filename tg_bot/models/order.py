from __future__ import annotations
__all__ = ["Order"]
from tortoise import Model
from tortoise.fields import UUIDField, CharField

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor


class Order(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing an order in the system.
    
    :ivar id: UUID primary key field for the order
    :ivar order_yookassa_id: CharField containing the YooKassa order ID (36 characters)
    """
    id = UUIDField(pk=True, unique=True)
    order_yookassa_id = CharField(36)

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the order visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_order()

    @classmethod
    async def create_order(cls, order_yookassa_id: str) -> "Order":
        """Creates a new order with the specified YooKassa ID.
        
        :param order_yookassa_id: The YooKassa order ID to associate with this order
        :return: The newly created Order instance
        """
        order = await cls.create(order_yookassa_id=order_yookassa_id)
        await order.save()
        return order