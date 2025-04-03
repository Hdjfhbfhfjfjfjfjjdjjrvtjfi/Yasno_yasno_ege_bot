__all__ = ["TestResultData"]
from pydantic import BaseModel, ConfigDict

from typing import Optional

from tg_bot.models import KnowledgeAssesment, TestResponse, TestQuestion, SchoolGrade


class TestResultData(BaseModel):
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    responses: list[TestResponse]
    questions: list[TestQuestion] | None = None
    knowledge_assesment: KnowledgeAssesment
    question_number: int = 0
    grade: Optional[SchoolGrade] = None
    def __init__(self, knowledge_assesment: KnowledgeAssesment, **data) -> None:
        super().__init__(knowledge_assesment=knowledge_assesment, responses= [], **data)

    @property
    def count_of_responses(self) -> int:
        return len(self.responses)

