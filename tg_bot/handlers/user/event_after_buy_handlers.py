__all__ = ["router"]
from aiogram import Router
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import InputMediaPhoto, FSInputFile

from tg_bot.filters.callback_data import (
    AfterBuyKnowledgeAssesmentPageCallbackData,
    SecondAfterBuyKnowledgeAssesmentGuidePageCallbackData
)
from tg_bot.keyboards import get_knowledge_assesment_after_buy_guide_keyboard, get_event_after_buy_keyboard
from tg_bot.utils.mixins import ConfigMixin
from tg_bot.utils.texts import (
    get_knowledge_assesment_after_buy_page_text,
    get_knowledge_assesment_after_buy_second_guide_page_text,
)


router: Router = Router()

@router.callback_query(SecondAfterBuyKnowledgeAssesmentGuidePageCallbackData.filter())
class SecondAfterBuyKnowledgeAssesmentGuidePageHandler(CallbackQueryHandler, ConfigMixin):
    async def handle(self):
        await self.event.message.edit_media(InputMediaPhoto(media=FSInputFile(self.config.second_guide_image_path)))
        await self.event.message.edit_caption(
            caption=get_knowledge_assesment_after_buy_second_guide_page_text()
        )
        await self.event.message.edit_reply_markup(
            reply_markup=get_knowledge_assesment_after_buy_guide_keyboard(AfterBuyKnowledgeAssesmentPageCallbackData)
        )


@router.callback_query(AfterBuyKnowledgeAssesmentPageCallbackData.filter())
class AfterBuyKnowledgeAssesmentPageHandler(CallbackQueryHandler):
    async def handle(self):
        await self.event.message.delete()
        await self.bot.send_message(
            chat_id=self.event.message.chat.id,
            text=get_knowledge_assesment_after_buy_page_text(),
            reply_markup=get_event_after_buy_keyboard()
        )

