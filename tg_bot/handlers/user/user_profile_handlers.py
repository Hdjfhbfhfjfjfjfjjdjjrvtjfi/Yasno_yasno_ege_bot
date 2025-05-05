__all__ = ["router"]
from typing import Optional, Any

from aiogram import Router
from aiogram.handlers import CallbackQueryHandler

from tg_bot.filters.callback_data import UserProfilePageCallbackData
from tg_bot.utils.texts import get_user_profile_page_text
from tg_bot.utils.wrap_classes import KnowledgeAssesmentProfile, ExcursionProfile
from tg_bot.keyboards import get_user_profile_page_keyboard
from tg_bot.models import User, BotUserProfile


router: Router = Router()

@router.callback_query(UserProfilePageCallbackData.filter())
class UserProfilePageHandler(CallbackQueryHandler):
    async def handle(self) -> None:
        user: User = await User.get_user_by_id(self.message.chat.id)
        user_profile: BotUserProfile = await user.get_user_profile()
        excursion_data: Optional[tuple[str, str]] = await self._get_excursion_data(user_profile)
        knowledge_assesment_data: Optional[tuple[str, str]] = await self._get_knowledge_assesment_data(user_profile)
        await self.message.edit_text(
            text=get_user_profile_page_text(excursion_data, knowledge_assesment_data)
        )
        await self.message.edit_reply_markup(
            reply_markup=get_user_profile_page_keyboard()
        )

    @staticmethod
    async def _get_excursion_data(
        user_profile: BotUserProfile
    ) -> Optional[tuple[str, str]]:
        if not await user_profile.has_excursion():
            return None
        
        excursion_profile: ExcursionProfile = await user_profile.get_excursion_profile()
        excursion: Any = excursion_profile.excursion
        return excursion.date, excursion.address

    @staticmethod
    async def _get_knowledge_assesment_data(
        user_profile: BotUserProfile
    ) -> Optional[tuple[str, str]]:
        if not await user_profile.has_knowledge_assesment():
            return None
        
        knowledge_assesment_profile: KnowledgeAssesmentProfile = await user_profile.get_knowledge_assesment_profile()
        knowledge_assesment: Any = knowledge_assesment_profile.knowledge_assesment
        return knowledge_assesment.date, knowledge_assesment.webinar_link
    