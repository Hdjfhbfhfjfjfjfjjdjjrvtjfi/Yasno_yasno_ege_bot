from __future__ import annotations
__all__ = ["TestQuestion"]
from tortoise import Model, BaseDBAsyncClient
from tortoise.fields import UUIDField, TextField, ManyToManyField

from typing import Optional, TYPE_CHECKING

from tg_bot.models import TestAnswer, SchoolGrade
from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor
    from tg_bot.utils.data_objects import QuestionData


class TestQuestion(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a test question in the system.
    
    :ivar id: UUID primary key field for the question
    :ivar description: Text field containing the question description
    :ivar answers: Many-to-many relationship with TestAnswer model
    """
    id = UUIDField(pk=True)
    description = TextField()
    answers = ManyToManyField("models.TestAnswer", related_name="_question")

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the test question visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_test_question()

    async def delete(self, using_db: Optional[BaseDBAsyncClient] = None) -> None:
        """Deletes the test question and all associated answers.
        
        :param using_db: Optional database connection to use
        :return: None
        """
        await self.answers.all().delete()
        await super().delete()

    @classmethod
    async def create_test_question(cls, question_data: QuestionData) -> "TestQuestion":
        """Creates a new test question with associated answers and school grade.
        
        :param question_data: QuestionData object containing the question details
        :return: The newly created TestQuestion instance
        """
        test_question = await cls.create(description=question_data.description)
        school_grade = await SchoolGrade.get_by_id(question_data.school_grade)
        answers = [await TestAnswer.create_test_answer(description)
                   for description in question_data.answers_descriptions]
        await school_grade.questions.add(test_question)
        await test_question.answers.add(*answers)
        await test_question.save()
        return test_question
