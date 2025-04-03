from __future__ import annotations
__all__ = ["TestAnswer"]
from tortoise.models import Model
from tortoise.fields import UUIDField, ManyToManyRelation, TextField

from typing import TYPE_CHECKING, Optional

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor


class TestAnswer(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = UUIDField(pk=True, unique=True)
    description = TextField()
    _question: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_test_answer()

    async def get_question(self):
        return await self._question.all().first()

    @classmethod
    async def get_by_id(cls, test_answer_id: str) -> Optional["TestAnswer"]:
        return await cls.get_or_none(id=test_answer_id)

    @classmethod
    async def create_test_answer(cls, description: str) -> "TestAnswer":
        test_answer = await cls.create(description=description)
        await test_answer.save()
        return test_answer
