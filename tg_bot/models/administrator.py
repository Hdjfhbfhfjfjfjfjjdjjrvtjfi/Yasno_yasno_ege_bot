from __future__ import annotations
__all__ = ["Administrator"]
from tortoise import Model
from tortoise.fields import IntField, BooleanField

from typing import TYPE_CHECKING, Optional

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor


class Administrator(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = IntField(pk=True)
    can_manipulate_administrator_table = BooleanField()

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_administrator()

    @classmethod
    async def get_administrator_by_id(cls, administrator_id: int) -> Optional["Administrator"]:
        return await cls.get_or_none(id=administrator_id)

    @classmethod
    async def create_administrator(cls, administrator_id: int) -> "Administrator":
        return await cls.create(id=administrator_id, can_manipulate_administrator_table=False)