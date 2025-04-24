from __future__ import annotations
__all__ = ["TestResult"]
from tortoise import Model
from tortoise.fields import UUIDField, ManyToManyField, ForeignKeyField, ManyToManyRelation

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor
    from tg_bot.models import BotUserProfile
    from tg_bot.utils.data_objects import TestResultData


class TestResult(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a test result in the system.
    
    :ivar id: UUID primary key field for the result
    :ivar grade: Foreign key relationship with SchoolGrade model
    :ivar test_responses: Many-to-many relationship with TestResponse model
    :ivar _bot_user_profiles: Many-to-many relationship with BotUserProfile model
    """
    id = UUIDField(pk=True, unique=True)
    grade = ForeignKeyField("models.SchoolGrade")
    test_responses = ManyToManyField("models.TestResponse")
    _bot_user_profiles: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the test result visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_test_result()

    @classmethod
    async def create_test_result(cls, test_result_data: TestResultData) -> "TestResult":
        """Creates a new test result with associated responses.
        
        :param test_result_data: TestResultData object containing the result details
        :return: The newly created TestResult instance
        """
        test_result = await cls.create(grade=test_result_data.grade)
        for response in test_result_data.responses:
            await test_result.test_responses.add(response)
        await test_result.save()
        return test_result

    async def get_bot_user_profile(self) -> BotUserProfile:
        """Retrieves the associated bot user profile for this test result.
        
        :return: The BotUserProfile instance associated with this result
        """
        return await self._bot_user_profiles.all().first()