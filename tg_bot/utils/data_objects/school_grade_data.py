__all__ = ["SchoolGradeData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict


class SchoolGradeData(BaseModel):
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    grade: int | None = None
    message: Message | None = None