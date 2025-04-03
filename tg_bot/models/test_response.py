from __future__ import annotations
__all__ = ["TestResponse"]
from tortoise import Model
from tortoise.fields import UUIDField, ForeignKeyField

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor
    from tg_bot.models import TestQuestion, TestAnswer


class TestResponse(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = UUIDField(pk=True)
    question = ForeignKeyField("models.TestQuestion")
    answer = ForeignKeyField("models.TestAnswer")

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_test_response()

    @classmethod
    async def create_test_response(cls, question: TestQuestion, answer: TestAnswer) -> "TestResponse":
        response = await cls.create(question=question, answer=answer)
        await response.save()
        return response