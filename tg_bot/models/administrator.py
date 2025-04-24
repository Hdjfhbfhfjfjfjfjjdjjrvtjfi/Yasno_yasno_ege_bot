from __future__ import annotations
__all__ = ["Administrator"]
from tortoise import Model
from tortoise.fields import IntField, BooleanField

from typing import TYPE_CHECKING, Optional

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor


class Administrator(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing an administrator in the system.
    
    :ivar id: Primary key field for the administrator
    :ivar can_manipulate_administrator_table: Boolean flag indicating if the administrator
        has permissions to manage other administrators
    """
    id = IntField(pk=True)
    can_manipulate_administrator_table = BooleanField()

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the administrator visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_administrator()

    @classmethod
    async def get_administrator_by_id(cls, administrator_id: int) -> Optional["Administrator"]:
        """Retrieves an administrator by their ID.
        
        :param administrator_id: The ID of the administrator to retrieve
        :return: The Administrator instance if found, None otherwise
        """
        return await cls.get_or_none(id=administrator_id)

    @classmethod
    async def create_administrator(cls, administrator_id: int) -> "Administrator":
        """Creates a new administrator with default permissions.
        
        :param administrator_id: The ID for the new administrator
        :return: The newly created Administrator instance
        """
        return await cls.create(id=administrator_id, can_manipulate_administrator_table=False)