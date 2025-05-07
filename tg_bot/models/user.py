from __future__ import annotations
__all__ = ["User"]
from tortoise import Model
from tortoise.fields import IntField, TextField, CharField, ManyToManyField
from tortoise.backends.base.client import BaseDBAsyncClient

from typing import Optional, TYPE_CHECKING

from tg_bot.models import BotUserProfile
from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor
    from tg_bot.utils.data_objects import UserData
    from tg_bot.models import Order


class User(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a user in the system.
    
    :ivar id: Integer primary key field for the user
    :ivar name_last_name_surname: Text field containing the user's full name
    :ivar phone_number: Char field containing the user's phone number (max 12 characters)
    :ivar _bot_user_profile: Many-to-many relationship with BotUserProfile model
    :ivar _order: Many-to-many relationship with Order model
    """
    id = IntField(pk=True, unique=True)
    name_last_name_surname = TextField()
    phone_number = CharField(max_length=12)
    _bot_user_profile = ManyToManyField("models.BotUserProfile", related_name="_users")
    _order = ManyToManyField("models.Order")

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the user visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_user()

    async def delete(self, using_db: Optional[BaseDBAsyncClient] = None) -> None:
        """Deletes the user and all associated bot user profiles.
        
        :param using_db: Optional database connection to use
        :return: None
        """
        await self._bot_user_profile.all().delete()
        await super().delete(using_db=using_db)

    async def get_user_profile(self) -> BotUserProfile:
        """Retrieves the associated bot user profile for this user.
        
        :return: The BotUserProfile instance associated with this user
        """
        return await self._bot_user_profile.all().first()

    async def get_order(self) -> Optional[Order]:
        """Retrieves the associated order for this user.
        
        :return: The Order instance associated with this user, None if no order exists
        """
        return await self._order.all().first()

    async def set_order(self, value: Order) -> None:
        """Sets the order for this user.
        
        :param value: The Order instance to associate with this user
        :return: None
        """
        await self._order.add(value)

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional["User"]:
        """Retrieves a user by their ID.
        
        :param user_id: The ID of the user to retrieve
        :return: The User instance if found, None otherwise
        """
        return await cls.get_or_none(id=user_id)

    @classmethod
    async def create_user(cls, user_data: UserData) -> "User":
        """Creates a new user with the provided data.
        
        :param user_data: UserData object containing the user details
        :return: The newly created User instance
        """
        user = await cls.create(
            id=user_data.user_id,
            name_last_name_surname=user_data.name_last_name_surname,
            phone_number=user_data.phone_number
        )
        bot_user_profile = await BotUserProfile.create_bot_user_profile()
        await user._bot_user_profile.add(bot_user_profile)
        await user.save()
        return user




