__all__ = ["EventData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict

from tg_bot.utils.interfaces import IEvent, IDataObject


class EventData(BaseModel, IDataObject):
    """Data class for storing and managing event-related information.

    This class represents event data with various attributes for scheduling,
    pricing, and capacity management. It uses Pydantic for data validation
    and serialization.

    :ivar event_type: Type of the event (e.g., excursion, knowledge assessment)
    :ivar year: Year component of the event date
    :ivar month: Month component of the event date
    :ivar day: Day component of the event date
    :ivar hour: Hour component of the event time
    :ivar minute: Minute component of the event time
    :ivar max_count_of_buyings: Maximum number of purchases allowed
    :ivar price: Price of the event
    :ivar string_field: Additional string field for event-specific data
    :ivar last_message: Last related message from the bot
    """
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    event_type: type[IEvent] | None = None  # Type of the event (e.g., excursion, knowledge assessment)
    year: int | None = None  # Year component of the event date
    month: int | None = None  # Month component of the event date
    day: int | None = None  # Day component of the event date
    hour: int | None = None  # Hour component of the event time
    minute: int | None = None  # Minute component of the event time
    max_count_of_buyings: int | None = None  # Maximum number of purchases allowed
    price: int | None = None  # Price of the event
    string_field: str | None = None  # Additional string field for event-specific data

    async def create_model_instance(self) -> None:
        await self.event_type.create_event(self)