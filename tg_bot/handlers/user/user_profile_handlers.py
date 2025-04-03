__all__ = ["router"]
from aiogram import Router
from aiogram.types import CallbackQuery

from tg_bot.filters.callback_data import UserProfilePageCallbackData
from tg_bot.utils.texts import get_user_profile_page_text
from tg_bot.keyboards import get_user_profile_page_keyboard
from tg_bot.models import User


router: Router = Router()


@router.callback_query(UserProfilePageCallbackData.filter())
async def user_profile_page_handler(call: CallbackQuery) -> None:
    user_profile = await (await User.get_user_by_id(call.message.chat.id)).get_user_profile()
    excursion = None
    knowledge_assesment = None
    if await user_profile.has_excursion():
        excursion = (await user_profile.get_excursion_profile()).excursion
        excursion = excursion.date, excursion.address
    if await user_profile.has_knowledge_assesment():
        knowledge_assesment = (await user_profile.get_knowledge_assesment_profile()).knowledge_assesment
        knowledge_assesment = knowledge_assesment.date, knowledge_assesment.webinar_link
    await call.message.edit_text(
        text=get_user_profile_page_text(excursion, knowledge_assesment)
    )
    await call.message.edit_reply_markup(
        reply_markup=get_user_profile_page_keyboard()
    )