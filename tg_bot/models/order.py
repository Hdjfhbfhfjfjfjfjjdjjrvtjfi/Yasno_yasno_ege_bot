from __future__ import annotations
__all__ = ["Order"]
from tortoise import Model
from tortoise.fields import UUIDField, CharField

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor


class Order(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = UUIDField(pk=True, unique=True)
    order_yookassa_id = CharField(36)

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_order()

    @classmethod
    async def create_order(cls, order_yookassa_id: str) -> "Order":
        order = await cls.create(order_yookassa_id=order_yookassa_id)
        await order.save()
        return order