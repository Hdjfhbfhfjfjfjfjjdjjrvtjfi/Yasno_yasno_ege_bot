__all__ = ["UserData"]
from pydantic import BaseModel, ConfigDict

from tg_bot.utils.interfaces import IDataObject
from tg_bot.models import User


class UserData(BaseModel, IDataObject):
    """Data class for storing and validating user information.

    This class represents user data with validation for phone numbers and full names.
    It uses Pydantic for data validation and serialization.

    :ivar user_id: The user's unique identifier
    :ivar name_last_name_surname: The user's full name
    :ivar phone_number: The user's phone number
    :ivar last_message: Last related message from the bot
    """

    async def create_model_instance(self) -> None:
        await User.create_user(self)

    model_config = ConfigDict(validate_assignment=True)
    user_id: int
    name_last_name_surname: str | None = None
    phone_number: str | None = None
