from __future__ import annotations
__all__ = ["BotUserProfile"]
from tortoise import Model
from tortoise.fields import UUIDField, ManyToManyField, ManyToManyRelation

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.wrap_classes import ExcursionProfile, KnowledgeAssesmentProfile
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor
    from tg_bot.models import User


class BotUserProfile(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = UUIDField(pk=True, unique=True)
    _excursion = ManyToManyField("models.Excursion", related_name="bot_user_profiles")
    _knowledge_assesment = ManyToManyField("models.KnowledgeAssesment", related_name="bot_user_profiles")
    _test_result = ManyToManyField("models.TestResult", related_name="_bot_user_profiles")
    _users: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_bot_user_profile()

    async def get_user(self) -> User:
        return await self._users.all().first()

    async def get_knowledge_assesment_profile(self) -> KnowledgeAssesmentProfile:
        return KnowledgeAssesmentProfile(
            await self._knowledge_assesment.all().first(),
            await self._test_result.all().first()
        )

    async def set_knowledge_assesment_profile(self, value: KnowledgeAssesmentProfile) -> None:
        await self._knowledge_assesment.clear()
        await self._test_result.clear()
        await self._knowledge_assesment.add(value.knowledge_assesment)
        await self._test_result.add(value.test_result)

    async def delete_knowledge_assesment_profile(self) -> None:
        await self._knowledge_assesment.clear()
        await self._test_result.clear()

    async def get_excursion_profile(self) -> ExcursionProfile:
        return ExcursionProfile(await self._excursion.all().first())

    async def set_excursion_profile(self, excursion_profile: ExcursionProfile) -> None:
        await self._excursion.clear()
        await self._excursion.add(excursion_profile.excursion)

    async def delete_excursion_profile(self) -> None:
        await self._excursion.clear()

    async def has_excursion(self) -> bool:
        return (await self._excursion.all().count()) > 0

    async def has_knowledge_assesment(self) -> bool:
        return (await self._knowledge_assesment.all().count()) > 0

    @classmethod
    async def create_bot_user_profile(cls) -> "BotUserProfile":
        bot_user_profile = BotUserProfile()
        await bot_user_profile.save()
        return bot_user_profile