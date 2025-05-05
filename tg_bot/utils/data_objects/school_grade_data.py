__all__ = ["SchoolGradeData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict

from tg_bot.models import SchoolGrade
from tg_bot.utils.interfaces import IDataObject


class SchoolGradeData(BaseModel, IDataObject):
    """Data class for storing and managing school grade information.

    This class represents school grade data with validation
    It uses Pydantic for data validation and serialization.

    :ivar grade: The school grade value
    :ivar message: Last related message from the bot
    """
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    grade: int | None = None  # The school grade value

    async def create_model_instance(self) -> None:
        await SchoolGrade.create_school_grade(self)