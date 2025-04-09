__all__ = ["EventData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict

from tg_bot.utils.interfaces import IEvent


class EventData(BaseModel):
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    event_type: type[IEvent] | None = None
    year: int | None = None
    month: int | None = None
    day: int | None = None
    hour: int | None = None
    minute: int | None = None
    max_count_of_buyings: int | None = None
    price: int | None = None
    string_field: str | None = None
    last_message: Message | None = None