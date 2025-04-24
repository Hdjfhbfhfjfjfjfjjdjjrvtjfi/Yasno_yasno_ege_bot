from __future__ import annotations
__all__ = ["TestAnswer"]
from tortoise.models import Model
from tortoise.fields import UUIDField, ManyToManyRelation, TextField

from typing import TYPE_CHECKING, Optional

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor


class TestAnswer(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a test answer in the system.
    
    :ivar id: UUID primary key field for the answer
    :ivar description: Text field containing the answer description
    :ivar _question: Many-to-many relationship with TestQuestion model
    """
    id = UUIDField(pk=True, unique=True)
    description = TextField()
    _question: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the test answer visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_test_answer()

    async def get_question(self):
        """Retrieves the associated test question for this answer.
        
        :return: The TestQuestion instance associated with this answer
        """
        return await self._question.all().first()

    @classmethod
    async def get_by_id(cls, test_answer_id: str) -> Optional["TestAnswer"]:
        """Retrieves a test answer by its ID.
        
        :param test_answer_id: The UUID of the answer to retrieve
        :return: The TestAnswer instance if found, None otherwise
        """
        return await cls.get_or_none(id=test_answer_id)

    @classmethod
    async def create_test_answer(cls, description: str) -> "TestAnswer":
        """Creates a new test answer with the specified description.
        
        :param description: The text description of the answer
        :return: The newly created TestAnswer instance
        """
        test_answer = await cls.create(description=description)
        await test_answer.save()
        return test_answer
