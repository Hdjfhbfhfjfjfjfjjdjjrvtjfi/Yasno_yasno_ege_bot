from __future__ import annotations
__all__ = ["TestResponse"]
from tortoise import Model
from tortoise.fields import UUIDField, ForeignKeyField

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor
    from tg_bot.models import TestQuestion, TestAnswer


class TestResponse(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a test response in the system.
    
    :ivar id: UUID primary key field for the response
    :ivar question: Foreign key relationship with TestQuestion model
    :ivar answer: Foreign key relationship with TestAnswer model
    """
    id = UUIDField(pk=True)
    question = ForeignKeyField("models.TestQuestion")
    answer = ForeignKeyField("models.TestAnswer")

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the test response visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_test_response()

    @classmethod
    async def create_test_response(cls, question: TestQuestion, answer: TestAnswer) -> "TestResponse":
        """Creates a new test response linking a question with an answer.
        
        :param question: The TestQuestion instance
        :param answer: The TestAnswer instance
        :return: The newly created TestResponse instance
        """
        response = await cls.create(question=question, answer=answer)
        await response.save()
        return response