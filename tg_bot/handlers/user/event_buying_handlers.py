__all__ = ["router"]
from aiogram import Router

from typing import Optional

from aiogram.types import FSInputFile

from tg_bot.filters.callback_data import (
    ChooseEventDatePageCallbackData,
    ChooseEventDatePageSwitchKeyboardCallbackData,
    EventQuestionPageCallbackData,
    EventPageCallbackData,
    EventCheckPaymentPageCallbackData
)
from tg_bot.utils.data_objects import TestResultData
from tg_bot.utils.enums import EventEnum
from tg_bot.utils.interfaces import IEvent
from tg_bot.utils.mixins import StateMixin
from tg_bot.utils.texts import (
    get_excursion_question_page_text,
    get_excursion_pay_page_text,
    get_knowledge_assesment_pay_page_text,
    get_knowledge_assesment_question_page_text,
    get_payment_fail_text,
    get_get_user_grade_text,
    get_payment_succed_go_back_text, get_excursion_after_buy_text
)
from tg_bot.keyboards import (
    get_choose_event_date_page_keyboard,
    get_event_question_page_keyboard,
    get_event_pay_page_keyboard,
    get_event_after_buy_keyboard,
    get_get_user_grade_keyboard
)
from tg_bot.models import Order, User, SchoolGrade, KnowledgeAssesment, Excursion
from tg_bot.services import PaymentService
from tg_bot.utils.wrap_classes import ExcursionProfile
from tg_bot.utils.constants import TEST_RESULT_DATA_ARGUMENT_NAME
from tg_bot.handlers.abstract_handlers import BaseEventHandler, BaseEventDateHandler

router: Router = Router()


@router.callback_query(ChooseEventDatePageCallbackData.filter())
class ChooseEventDatePageHandler(BaseEventDateHandler[ChooseEventDatePageCallbackData]):
    """Handler for choosing event date page."""
    
    async def handle(self) -> None:
        user = await self.get_user()
        order = await user.get_order()
        if (order is None or
                not (PaymentService.get_payment_by_id(order.order_yookassa_id)).is_succeed):
            if order is not None:
                await order.delete()
            data, count_of_clusters = await self.get_events_data(self.unpacked_callback_data.page_index)
            if self.unpacked_callback_data.event == EventEnum.knowledge_assesment:
                await self.message.edit_text(text=self.get_text())
                await self.message.edit_reply_markup(
                    reply_markup=get_choose_event_date_page_keyboard(
                        data, self.unpacked_callback_data.page_index, count_of_clusters, self.unpacked_callback_data.event
                    )
                )
            else:
                await self.event.message.delete()
                await self.bot.send_photo(
                    chat_id=self.event.message.chat.id,
                    photo=FSInputFile(self.config.excursion_image_path),
                    caption=self.get_text(),
                    reply_markup=get_choose_event_date_page_keyboard(
                        data, self.unpacked_callback_data.page_index, count_of_clusters, self.unpacked_callback_data.event
                    )
                )
        else:
            await self.event.answer(text=get_payment_succed_go_back_text())


@router.callback_query(ChooseEventDatePageSwitchKeyboardCallbackData.filter())
class ChooseEventDatePageSwitchHandler(BaseEventDateHandler[ChooseEventDatePageSwitchKeyboardCallbackData]):
    """Handler for switching between event date pages."""
    
    async def handle(self) -> None:
        data, count_of_clusters = await self.get_events_data(self.unpacked_callback_data.page_index)
        await self.message.edit_reply_markup(
            reply_markup=get_choose_event_date_page_keyboard(
                data,
                self.unpacked_callback_data.page_index,
                count_of_clusters,
                self.unpacked_callback_data.event
            )
        )


@router.callback_query(EventQuestionPageCallbackData.filter())
class EventQuestionPageHandler(BaseEventHandler[EventQuestionPageCallbackData]):
    """Handler for event question page."""
    
    async def handle(self) -> None:
        if self.unpacked_callback_data.event == EventEnum.knowledge_assesment:
            await self.message.edit_text(text=self.get_text())
            await self.message.edit_reply_markup(
                reply_markup=get_event_question_page_keyboard(
                    self.config.connection_link,
                    self.unpacked_callback_data.page_index,
                    self.unpacked_callback_data.event
                )
            )
        else:
            await self.event.message.delete()
            await self.bot.send_message(
                chat_id=self.event.message.chat.id,
                text=self.get_text(),
                reply_markup=get_event_question_page_keyboard(
                    self.config.connection_link,
                    self.unpacked_callback_data.page_index,
                    self.unpacked_callback_data.event
                )
            )

    def get_text(self) -> str:
        """Get the text for the event question page."""
        return (get_excursion_question_page_text()
               if self.unpacked_callback_data.event == EventEnum.excursion
               else get_knowledge_assesment_question_page_text())


@router.callback_query(EventPageCallbackData.filter())
class EventPageHandler(BaseEventHandler[EventPageCallbackData]):
    """Handler for event payment page."""
    
    async def handle(self) -> None:
        event = await self.event_model.get_by_id(self.unpacked_callback_data.id)
        user = await self.get_user()
        payment = PaymentService.create_payment(
            event.price,
            str(event.id),
            self.config.bot_link
        )
        order = await Order.create_order(payment.payment_id)
        await user.set_order(order)
        if self.unpacked_callback_data.event == EventEnum.knowledge_assesment:
            await self.message.edit_text(text=self.get_text(event))
            await self.message.edit_reply_markup(
                reply_markup=get_event_pay_page_keyboard(
                    payment.payment_url,
                    self.unpacked_callback_data.page_index,
                    self.unpacked_callback_data.event
                )
            )
        else:
            await self.event.message.delete()
            await self.bot.send_message(
                chat_id=self.event.message.chat.id,
                text=self.get_text(event),
                reply_markup=get_event_pay_page_keyboard(
                    payment.payment_url,
                    self.unpacked_callback_data.page_index,
                    self.unpacked_callback_data.event
                )
            )

    def get_text(self, event: IEvent) -> str:
        """Get the text for the event payment page."""
        text_func = (get_excursion_pay_page_text
                    if self.unpacked_callback_data.event == EventEnum.excursion
                    else get_knowledge_assesment_pay_page_text)
        return text_func(*event.get_pay_text_args())


@router.callback_query(EventCheckPaymentPageCallbackData.filter())
class EventCheckPaymentPageHandler(BaseEventHandler[EventCheckPaymentPageCallbackData], StateMixin):
    """Handler for checking event payment status."""
    
    async def handle(self) -> None:
        user = await self.get_user()
        event = await self.process_payment(user)
        if event is None:
            await self.event.answer(self.get_text())
            return
        if self.unpacked_callback_data.event == EventEnum.excursion:
            await self.postprocess_excursion_payment(event)
        else:
            await self.postprocess_knowledge_assesment_payment(event)

    async def process_payment(self, user: User) -> Optional[IEvent]:
        """Process payment and return event if successful."""
        order = await user.get_order()
        payment = PaymentService.get_payment_by_id(order.order_yookassa_id)
        if payment.is_succeed:
            event = await self.event_model.get_by_id(payment.label)
            await order.delete()
            return event
        return None

    def get_text(self, event: Optional[Excursion | KnowledgeAssesment] = None) -> str:
        """Get the text for the payment check page."""
        if event is None:
            return get_payment_fail_text()
        return (get_excursion_after_buy_text(event.address)
                if self.unpacked_callback_data.event == EventEnum.excursion
                else get_get_user_grade_text())

    async def postprocess_excursion_payment(self, event: Excursion):
        user = await self.get_user()
        user_profile = await user.get_user_profile()
        await user_profile.set_excursion_profile(ExcursionProfile(event))
        await self.message.edit_text(text=self.get_text(event))
        await self.message.edit_reply_markup(
            reply_markup=get_event_after_buy_keyboard()
        )

    async def postprocess_knowledge_assesment_payment(self, event: KnowledgeAssesment):
        grades = await SchoolGrade.get_grades_tuple()
        await self.state.update_data({
            TEST_RESULT_DATA_ARGUMENT_NAME: TestResultData(event)
        })
        await self.message.edit_text(text=self.get_text(event))
        await self.message.edit_reply_markup(
            reply_markup=get_get_user_grade_keyboard(grades)
        )
