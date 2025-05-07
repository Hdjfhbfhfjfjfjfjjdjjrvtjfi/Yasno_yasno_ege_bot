from __future__ import annotations
__all__ = ["BotUserProfile"]
from tortoise import Model
from tortoise.fields import UUIDField, ManyToManyField, ManyToManyRelation

from typing import TYPE_CHECKING

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.wrap_classes import ExcursionProfile, KnowledgeAssesmentProfile
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor
    from tg_bot.models import User


class BotUserProfile(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a user's profile in the bot system.
    
    This class manages a user's profile including their excursion bookings,
    knowledge assessments, and test results.

    :ivar id: UUID primary key field for the profile
    :ivar _excursion: Many-to-many relationship with Excursion model
    :ivar _knowledge_assesment: Many-to-many relationship with KnowledgeAssesment model
    :ivar _test_result: Many-to-many relationship with TestResult model
    :ivar _users: Many-to-many relationship with User model
    """
    id = UUIDField(pk=True, unique=True)
    _excursion = ManyToManyField("models.Excursion", related_name="bot_user_profiles")
    _knowledge_assesment = ManyToManyField("models.KnowledgeAssesment", related_name="bot_user_profiles")
    _test_result = ManyToManyField("models.TestResult", related_name="_bot_user_profiles")
    _users: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the bot user profile visit method.
        
        This method implements the visitor pattern by accepting a visitor object
        and calling its corresponding visit method for this model.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_bot_user_profile()

    async def get_user(self) -> User:
        """Retrieves the associated user for this profile.
        
        :return: The User instance associated with this profile
        """
        return await self._users.all().first()

    async def get_knowledge_assesment_profile(self) -> KnowledgeAssesmentProfile:
        """Retrieves the knowledge assessment profile for this user.
        
        :return: KnowledgeAssesmentProfile containing the assessment and test result
        """
        return KnowledgeAssesmentProfile(
            await self._knowledge_assesment.all().first(),
            await self._test_result.all().first()
        )

    async def set_knowledge_assesment_profile(self, value: KnowledgeAssesmentProfile) -> None:
        """Sets the knowledge assessment profile for this user.
        
        :param value: The new KnowledgeAssesmentProfile to set
        :return: None
        """
        await self._knowledge_assesment.clear()
        await self._test_result.clear()
        await self._knowledge_assesment.add(value.knowledge_assesment)
        await self._test_result.add(value.test_result)

    async def get_excursion_profile(self) -> ExcursionProfile:
        """Retrieves the excursion profile for this user.
        
        :return: ExcursionProfile containing the associated excursion
        """
        return ExcursionProfile(await self._excursion.all().first())

    async def set_excursion_profile(self, excursion_profile: ExcursionProfile) -> None:
        """Sets the excursion profile for this user.
        
        :param excursion_profile: The new ExcursionProfile to set
        :return: None
        """
        await self._excursion.clear()
        await self._excursion.add(excursion_profile.excursion)

    async def has_excursion(self) -> bool:
        """Checks if the user has any excursions booked.
        
        :return: True if the user has at least one excursion, False otherwise
        """
        return (await self._excursion.all().count()) > 0

    async def has_knowledge_assesment(self) -> bool:
        """Checks if the user has any knowledge assessments.
        
        :return: True if the user has at least one knowledge assessment, False otherwise
        """
        return (await self._knowledge_assesment.all().count()) > 0

    async def delete_test_result(self) -> None:
        """Deletes the test result associated with this profile.
        
        :return: None
        """
        test_result = await self._test_result.all().first()
        await self._test_result.clear()
        await test_result.delete()

    @classmethod
    async def create_bot_user_profile(cls) -> "BotUserProfile":
        """Creates a new bot user profile.
        
        :return: The newly created BotUserProfile instance
        """
        bot_user_profile = BotUserProfile()
        await bot_user_profile.save()
        return bot_user_profile