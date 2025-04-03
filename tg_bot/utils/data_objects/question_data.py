__all__ = ["QuestionData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict


class QuestionData(BaseModel):
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    description: str | None = None
    school_grade: int | None = None
    max_count_of_answers: int | None = None
    last_message: Message | None = None
    answers_descriptions: list[str]

    def __init__(self, **data):
        super().__init__(answers_descriptions=[], **data)

    @property
    def count_of_answers(self) -> int:
        return len(self.answers_descriptions)