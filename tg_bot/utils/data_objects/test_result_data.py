__all__ = ["TestResultData"]
from pydantic import BaseModel, ConfigDict

from typing import Optional

from tg_bot.models import KnowledgeAssesment, TestResponse, TestQuestion, SchoolGrade


class TestResultData(BaseModel):
    """Data class for storing and managing test result information.

    This class represents test result data including responses, questions,
    and assessment details. It uses Pydantic for data validation and serialization.

    :ivar responses: List of test responses
    :ivar questions: List of test questions
    :ivar knowledge_assesment: Associated knowledge assessment
    :ivar question_number: Current question number in the test
    :ivar grade: School grade associated with the test
    """
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    responses: list[TestResponse]  # List of test responses
    questions: list[TestQuestion] | None = None  # List of test questions
    knowledge_assesment: KnowledgeAssesment  # Associated knowledge assessment
    question_number: int = 0  # Current question number in the test
    grade: Optional[SchoolGrade] = None  # School grade associated with the test

    def __init__(self, knowledge_assesment: KnowledgeAssesment, **data) -> None:
        """Initializes a new TestResultData instance.

        :param knowledge_assesment: The knowledge assessment this test result belongs to
        :param data: Additional data to initialize the test result with
        :return: None
        """
        super().__init__(knowledge_assesment=knowledge_assesment, responses=[], **data)

    @property
    def count_of_responses(self) -> int:
        """Gets the current number of responses in the test result.

        :return: The number of responses currently recorded
        """
        return len(self.responses)

