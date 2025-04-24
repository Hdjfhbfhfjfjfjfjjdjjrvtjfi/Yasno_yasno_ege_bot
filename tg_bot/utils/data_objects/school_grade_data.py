__all__ = ["SchoolGradeData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict


class SchoolGradeData(BaseModel):
    """Data class for storing and managing school grade information.

    This class represents school grade data with validation
    It uses Pydantic for data validation and serialization.

    :ivar grade: The school grade value
    :ivar message: Last related message from the bot
    """
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    grade: int | None = None  # The school grade value
    message: Message | None = None  # Last related message from the bot