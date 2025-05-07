__all__ = ["QuestionData"]
from aiogram.types import Message

from pydantic import BaseModel, ConfigDict

from tg_bot.models import TestQuestion
from tg_bot.utils.interfaces import IDataObject


class QuestionData(BaseModel, IDataObject):
    """Data class for storing and managing test question information.

    This class represents test question data including the question description,
    target school grade, and associated answers. It uses Pydantic for data
    validation and serialization.

    :ivar description: The text of the question
    :ivar school_grade: Target school grade for the question
    :ivar max_count_of_answers: Maximum number of allowed answers
    :ivar last_message: Last related message from the bot
    :ivar answers_descriptions: List of answer descriptions
    """
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    description: str | None = None  # The text of the question
    school_grade: int | None = None  # Target school grade for the question
    max_count_of_answers: int | None = None  # Maximum number of allowed answers
    answers_descriptions: list[str]  # List of answer descriptions

    def __init__(self, **data):
        """Initializes a new QuestionData instance.

        :param data: Additional data to initialize the question with
        :return: None
        """
        super().__init__(answers_descriptions=[], **data)

    @property
    def count_of_answers(self) -> int:
        """Gets the current number of answers for this question.

        :return: The number of answers currently associated with the question
        """
        return len(self.answers_descriptions)

    async def create_model_instance(self) -> None:
        await TestQuestion.create_test_question(self)