from __future__ import annotations
__all__ = ["User"]
from tortoise import Model
from tortoise.fields import IntField, TextField, CharField, ManyToManyField
from tortoise.backends.base.client import BaseDBAsyncClient

from typing import Optional, TYPE_CHECKING

from tg_bot.models import BotUserProfile
from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor
    from tg_bot.utils.data_objects import UserData
    from tg_bot.models import Order


class User(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = IntField(pk=True, unique=True)
    name_last_name_surname = TextField()
    phone_number = CharField(max_length=12)
    _bot_user_profile = ManyToManyField("models.BotUserProfile", related_name="_users")
    _order = ManyToManyField("models.Order")

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_user()

    async def delete(self, using_db: Optional[BaseDBAsyncClient] = None) -> None:
        await self._bot_user_profile.all().delete()
        await super().delete(using_db=using_db)

    async def get_user_profile(self) -> BotUserProfile:
        return await self._bot_user_profile.all().first()

    async def get_order(self) -> Optional[Order]:
        return await self._order.all().first()

    async def set_order(self, value: Order) -> None:
        await self._order.add(value)

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional["User"]:
        return await cls.get_or_none(id=user_id)

    @classmethod
    async def create_user(cls, user_data: UserData) -> "User":
        user = await cls.create(
            id=user_data.user_id,
            name_last_name_surname=user_data.name_last_name_surname,
            phone_number=user_data.phone_number
        )
        bot_user_profile = await BotUserProfile.create_bot_user_profile()
        await user._bot_user_profile.add(bot_user_profile)
        await user.save()
        return user




