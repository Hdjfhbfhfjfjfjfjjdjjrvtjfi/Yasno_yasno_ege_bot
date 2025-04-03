from __future__ import annotations
__all__ = ["TestResult"]
from tortoise import Model
from tortoise.fields import UUIDField, ManyToManyField, ForeignKeyField, ManyToManyRelation

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor
    from tg_bot.models import BotUserProfile
    from tg_bot.utils.data_objects import TestResultData


class TestResult(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = UUIDField(pk=True, unique=True)
    grade = ForeignKeyField("models.SchoolGrade")
    test_responses = ManyToManyField("models.TestResponse")
    _bot_user_profiles: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_test_result()

    @classmethod
    async def create_test_result(cls, test_result_data: TestResultData) -> "TestResult":
        test_result = await cls.create(grade=test_result_data.grade)
        for response in test_result_data.responses:
            await test_result.test_responses.add(response)
        await test_result.save()
        return test_result

    async def get_bot_user_profile(self) -> BotUserProfile:
        return await self._bot_user_profiles.all().first()