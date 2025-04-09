__all__ = ["router"]
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from datetime import datetime

from typing import Callable

from tg_bot.filters.callback_data import(ChooseEventDatePageCallbackData, ChooseEventDatePageSwitchKeyboardCallbackData,
                                         EventQuestionPageCallbackData, EventPageCallbackData,
                                         EventCheckPaymentPageCallbackData)
from tg_bot.utils.data_objects import TestResultData
from tg_bot.utils.enums import EventEnum
from tg_bot.utils.interfaces import IEvent
from tg_bot.utils.texts import (get_choose_excursion_date_page_text, get_excursion_question_page_text,
                                get_excursion_pay_page_text, get_main_menu_page_text,
                                get_knowledge_assesment_pay_page_text, get_knowledge_assesment_question_page_text,
                                get_choose_knowledge_assesment_date_page_text, get_payment_fail_text,
                                get_get_user_grade_text, get_payment_succed_go_back_text)
from tg_bot.utils.config import Config
from tg_bot.keyboards import (get_choose_event_date_page_keyboard, get_event_question_page_keyboard,
                              get_event_pay_page_keyboard, get_main_menu_page_keyboard, get_get_user_grade_keyboard)
from tg_bot.models import Excursion, Order, User, KnowledgeAssesment, SchoolGrade
from tg_bot.services import PaymentService
from tg_bot.utils.wrap_classes import ExcursionProfile
from tg_bot.utils.constants import KNOWLEDGE_ASSESMENT_DATA_ARGUMENT_NAME

router: Router = Router()


@router.callback_query(ChooseEventDatePageCallbackData.filter())
async def choose_event_date_handler(call: CallbackQuery, config: Config,
                                        callback_data: ChooseEventDatePageCallbackData) -> None:
    async def process_event(model: type[IEvent], text: str) -> None:
        events, count_of_clusters = await model.get_cluster_and_count_of_clusters_by_date(
            datetime.now(),
            callback_data.page_index,
            config.cluster_size
        )

        data = tuple([(event.id, event.date, (await event.get_count_of_buyings()) < event.max_count_of_buyings)
                      for event in events])
        await call.message.edit_text(
            text=text
        )
        await call.message.edit_reply_markup(
            reply_markup=get_choose_event_date_page_keyboard(data, 0, count_of_clusters, callback_data.event)
        )
    user: User = await User.get_user_by_id(call.message.chat.id)
    if await user.get_order() is None:
        if callback_data.event == EventEnum.excursion:
            args = [Excursion, get_choose_excursion_date_page_text()]
        else:
            args = [KnowledgeAssesment, get_choose_knowledge_assesment_date_page_text()]
        await process_event(*args)
    else:
        await call.answer(text=get_payment_succed_go_back_text())

@router.callback_query(ChooseEventDatePageSwitchKeyboardCallbackData.filter())
async def choose_event_date_switch_page_handler(call: CallbackQuery, config: Config,
                                    callback_data: ChooseEventDatePageSwitchKeyboardCallbackData) -> None:
    async def process_event(model: type[IEvent]) -> None:
        events, count_of_clusters = await model.get_cluster_and_count_of_clusters_by_date(
            datetime.now(),
            callback_data.page_index,
            config.cluster_size
        )
        data = tuple([(event.id, event.date, (await event.get_count_of_buyings()) <= event.max_count_of_buyings) for event in events])
        await call.message.edit_reply_markup(
            reply_markup=get_choose_event_date_page_keyboard(data, callback_data.page_index, count_of_clusters, callback_data.event)
        )

    if callback_data.event == EventEnum.excursion:
        args = [Excursion]
    else:
        args = [KnowledgeAssesment]
    await process_event(*args)

@router.callback_query(EventQuestionPageCallbackData.filter())
async def event_question_page_handler(call: CallbackQuery, callback_data: EventQuestionPageCallbackData, config: Config
                                      ) -> None:
    async def process_event(text: str) -> None:
        await call.message.edit_text(
            text=text
        )
        await call.message.edit_reply_markup(
            reply_markup=get_event_question_page_keyboard(config.connection_link, callback_data.page_index, callback_data.event)
        )

    if callback_data.event == EventEnum.excursion:
        args = [get_excursion_question_page_text()]
    else:
        args = [get_knowledge_assesment_question_page_text()]
    await process_event(*args)

@router.callback_query(EventPageCallbackData.filter())
async def event_page_handler(call: CallbackQuery, config: Config, callback_data: EventPageCallbackData) -> None:
    async def process_event(model: type[IEvent], text_func: Callable) -> None:
        event = await model.get_by_id(callback_data.id)
        user = await User.get_user_by_id(call.message.chat.id)
        payment = PaymentService.create_payment(
            event.price,
            str(event.id),
            config.bot_link
        )
        order = await Order.create_order(payment.payment_id)
        await user.set_order(order)
        await call.message.edit_text(
            text=text_func(*event.get_pay_text_args())
        )
        await call.message.edit_reply_markup(
            reply_markup=get_event_pay_page_keyboard(payment.payment_url, callback_data.page_index, callback_data.event)
        )

    if callback_data.event == EventEnum.excursion:
        args = [Excursion, get_excursion_pay_page_text]
    else:
        args = [KnowledgeAssesment, get_knowledge_assesment_pay_page_text]
    await process_event(*args)

@router.callback_query(EventCheckPaymentPageCallbackData.filter())
async def event_check_payment_page_handler(call: CallbackQuery, config: Config, state: FSMContext,
                                           callback_data: EventCheckPaymentPageCallbackData) -> None:
    async def process_event(model: type[IEvent], user_: User) -> IEvent | None:
        order = await user_.get_order()
        payment = PaymentService.get_payment_by_id(order.order_yookassa_id)
        event = None
        if payment.is_succeed:
            event = await model.get_by_id(payment.label)
            await order.delete()
        return event
    user = await User.get_user_by_id(call.message.chat.id)
    user_profile = await user.get_user_profile()
    if callback_data.event == EventEnum.excursion:
        excursion: Excursion | None = await process_event(Excursion, user)
        if excursion is not None:
            await user_profile.set_excursion_profile(ExcursionProfile(excursion))
            await call.message.edit_text(
                text=get_main_menu_page_text()
            )
            await call.message.edit_reply_markup(
                reply_markup=get_main_menu_page_keyboard(
                    config.connection_link,
                    await user_profile.has_excursion(),
                    await user_profile.has_knowledge_assesment()
                )
            )
        else:
            await call.answer(get_payment_fail_text())
    else:
        knowledge_assesment: KnowledgeAssesment | None = await process_event(KnowledgeAssesment, user)
        if knowledge_assesment is not None:
            grades = await SchoolGrade.get_grades_tuple()
            await state.set_data({KNOWLEDGE_ASSESMENT_DATA_ARGUMENT_NAME: TestResultData(knowledge_assesment)})
            await call.message.edit_text(
                text=get_get_user_grade_text()
            )
            await call.message.edit_reply_markup(
                reply_markup=get_get_user_grade_keyboard(grades)
            )
        else:
            await call.answer(get_payment_fail_text())
