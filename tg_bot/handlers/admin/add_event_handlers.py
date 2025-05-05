__all__ = ["router"]
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import BotCommand, TelegramObject

from tg_bot.handlers.abstract_handlers import FormBaseHandler
from tg_bot.filters.commands import add_excursion_command, add_knowledge_assesment_command
from tg_bot.models import Excursion, KnowledgeAssesment
from tg_bot.utils.data_objects import EventData
from tg_bot.utils.constants import EVENT_DATA_ARGUMENT_NAME
from tg_bot.utils.message_builders import TextMessageBuilder
from tg_bot.states import AddEventFSM
from tg_bot.utils.mixins import CommandMixin
from tg_bot.utils.enums import HandlerTypeEnum
from tg_bot.utils.texts import (get_get_event_year_text, get_get_event_month_text, get_get_event_day_text,
                                get_get_event_hour_text, get_get_event_minute_text, get_get_event_price_text,
                                get_get_event_max_count_of_buyings_text, get_get_excursion_address_text,
                                get_get_knowledge_assesment_link_text)


router: Router = Router()

@router.message(Command(commands=[add_excursion_command, add_knowledge_assesment_command]))
class AddEventHandler(FormBaseHandler[EventData], CommandMixin, handler_type=HandlerTypeEnum.first_handler):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        await self.initialize_form_data(
            EventData(),
            TextMessageBuilder.send_new_message(
                get_get_event_year_text(),
                self.bot,
                self.event.chat.id
            ),
            AddEventFSM.year,
            EVENT_DATA_ARGUMENT_NAME,
            self.command
        )

    async def _process_command(self, command: BotCommand):
        if add_excursion_command.command == command.command:
            self.data_object.event_type = Excursion
        else:
            self.data_object.event_type = KnowledgeAssesment

@router.message(StateFilter(AddEventFSM.year))
class GetYearHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.year = await self.process_numeric_state(
            AddEventFSM.month,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_event_month_text())
        )

@router.message(StateFilter(AddEventFSM.month))
class GetMonthHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.month = await self.process_numeric_state(
            AddEventFSM.day,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_event_day_text())
        )

@router.message(StateFilter(AddEventFSM.day))
class GetDayHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.day = await self.process_numeric_state(
            AddEventFSM.hour,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_event_hour_text())
        )

@router.message(StateFilter(AddEventFSM.hour))
class GetHourHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.hour = await self.process_numeric_state(
            AddEventFSM.minute,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_event_minute_text())
        )

@router.message(StateFilter(AddEventFSM.minute))
class GetMinuteHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.minute = await self.process_numeric_state(
            AddEventFSM.price,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_event_price_text())
        )

@router.message(StateFilter(AddEventFSM.price))
class GetPriceHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.price = await self.process_numeric_state(
            AddEventFSM.max_count_of_buyings,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_event_max_count_of_buyings_text())
        )

@router.message(StateFilter(AddEventFSM.max_count_of_buyings))
class GetMaxCountHandler(FormBaseHandler[EventData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        if self.data_object.event_type == Excursion:
            text = get_get_excursion_address_text()
        else:
            text = get_get_knowledge_assesment_link_text()
        self.data_object.max_count_of_buyings = await self.process_numeric_state(
            AddEventFSM.string_field,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(text)
        )

@router.message(StateFilter(AddEventFSM.string_field))
class GetStringFieldHandler(FormBaseHandler[EventData], handler_type=HandlerTypeEnum.final_handler):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = EVENT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.string_field = await self.process_text_state(
            AddEventFSM.string_field,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message)
        )
        if self.data_object.string_field is not None:
            await self.data_object.create_model_instance()
