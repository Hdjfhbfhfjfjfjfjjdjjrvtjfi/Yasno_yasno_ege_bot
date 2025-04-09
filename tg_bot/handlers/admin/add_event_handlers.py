__all__ = ["router"]
from aiogram import Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State
from aiogram.types import Message, BotCommand
from aiogram.fsm.context import FSMContext

from tg_bot.filters.commands import add_excursion_command, add_knowledge_assesment_command
from tg_bot.models import Excursion, KnowledgeAssesment
from tg_bot.utils.data_objects import EventData
from tg_bot.utils.constants import EVENT_DATA_ARGUMENT_NAME
from tg_bot.states import AddEventFSM
from tg_bot.utils.texts import (get_get_event_year_text, get_get_event_month_text, get_get_event_day_text,
                                get_get_event_hour_text, get_get_event_minute_text, get_get_event_price_text,
                                get_get_event_max_count_of_buyings_text, get_get_excursion_address_text,
                                get_get_knowledge_assesment_link_text)


router: Router = Router()


async def process_event_numeric_state(message: Message, event_data: EventData, state: FSMContext, text: str,
                                      next_state: State) -> int | None:
    await message.delete()
    result: int | None
    if message.text is not None and message.text.isdigit():
        result = int(message.text)
    elif message.caption is not None and message.caption.isdigit():
        result = int(message.caption)
    if result is not None:
        await event_data.last_message.edit_text(
            text=text
        )
        await state.set_state(next_state)
    return result

@router.message(Command(commands=[add_excursion_command, add_knowledge_assesment_command]))
async def add_event_handler(message: Message, state: FSMContext, bot: Bot, command: BotCommand):
    await message.delete()
    event_data: EventData = EventData()
    if add_excursion_command.command == command.command:
        event_data.event_type = Excursion
    else:
        event_data.event_type = KnowledgeAssesment
    event_data.last_message = await bot.send_message(
        chat_id=message.chat.id,
        text=get_get_event_year_text()
    )
    await state.set_state(AddEventFSM.year)
    await state.set_data({EVENT_DATA_ARGUMENT_NAME: event_data})

@router.message(StateFilter(AddEventFSM.year))
async def get_year_handler(message: Message, state: FSMContext, event_data: EventData):
    event_data.year = await process_event_numeric_state(
        message,
        event_data,
        state,
        get_get_event_month_text(),
        AddEventFSM.month
    )

@router.message(StateFilter(AddEventFSM.month))
async def get_month_handler(message: Message, state: FSMContext, event_data: EventData):
    event_data.month = await process_event_numeric_state(
        message,
        event_data,
        state,
        get_get_event_day_text(),
        AddEventFSM.day
    )

@router.message(StateFilter(AddEventFSM.day))
async def get_day_handler(message: Message, state: FSMContext, event_data: EventData):
    event_data.day = await process_event_numeric_state(
        message,
        event_data,
        state,
        get_get_event_hour_text(),
        AddEventFSM.hour
    )

@router.message(StateFilter(AddEventFSM.hour))
async def get_hour_handler(message: Message, state: FSMContext, event_data: EventData):
    event_data.hour = await process_event_numeric_state(
        message,
        event_data,
        state,
        get_get_event_minute_text(),
        AddEventFSM.minute
    )

@router.message(StateFilter(AddEventFSM.minute))
async def get_minute_handler(message: Message, state: FSMContext, event_data: EventData):
    event_data.minute = await process_event_numeric_state(
        message,
        event_data,
        state,
        get_get_event_price_text(),
        AddEventFSM.price
    )

@router.message(StateFilter(AddEventFSM.price))
async def get_price_handler(message: Message, state: FSMContext, event_data: EventData):
    event_data.price = await process_event_numeric_state(
        message,
        event_data,
        state,
        get_get_event_max_count_of_buyings_text(),
        AddEventFSM.max_count_of_buyings
    )

@router.message(StateFilter(AddEventFSM.max_count_of_buyings))
async def get_max_count_of_buyings_handler(message: Message, state: FSMContext, event_data: EventData):
    if event_data.event_type == Excursion:
        text = get_get_excursion_address_text()
    else:
        text = get_get_knowledge_assesment_link_text()
    event_data.max_count_of_buyings = await process_event_numeric_state(
        message,
        event_data,
        state,
        text,
        AddEventFSM.string_field
    )

@router.message(StateFilter(AddEventFSM.string_field))
async def get_string_field_handler(message: Message, state: FSMContext, event_data: EventData):
    await message.delete()
    if message.text is not None:
        event_data.string_field = message.text
    elif message.caption is not None:
        event_data.string_field = message.caption
    if event_data.string_field is not None:
        await event_data.event_type.create_event(event_data)
        await event_data.last_message.delete()
        await state.clear()
