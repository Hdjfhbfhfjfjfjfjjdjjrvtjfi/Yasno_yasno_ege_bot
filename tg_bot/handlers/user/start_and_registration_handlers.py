__all__ = ["router"]
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter

from tg_bot import Config
from tg_bot.models import User
from tg_bot.filters.callback_data import GetUserDataPageCallbackData, MainMenuPageCallbackData
from tg_bot.utils.texts import (agreement_on_data_processing_page_text, get_main_menu_page_text,
                                get_get_user_name_full_name_surname_page_text, get_get_user_phone_number_page_text)
from tg_bot.utils.data_objects import UserData
from tg_bot.states import UserRegistrationFSM
from tg_bot.keyboards import agreement_on_data_processing_page_keyboard, get_main_menu_page_keyboard
from tg_bot.utils.constants import USER_DATA_ARGUMENT_NAME


router: Router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, config: Config) -> None:
    await message.delete()
    user = await User.get_user_by_id(message.from_user.id)
    if user is None:
        await bot.send_message(
            chat_id=message.chat.id,
            text=agreement_on_data_processing_page_text(),
            reply_markup=agreement_on_data_processing_page_keyboard(config.agreement_on_data_processing_link),
        )
    else:
        user_profile = await user.get_user_profile()
        await bot.send_message(
            chat_id=message.chat.id,
            text=get_main_menu_page_text(),
            reply_markup=get_main_menu_page_keyboard(
                config.connection_link,
                await user_profile.has_excursion(),
                await user_profile.has_knowledge_assesment()
            )
        )

@router.callback_query(MainMenuPageCallbackData.filter())
async def main_menu_handler(call: CallbackQuery, config: Config) -> None:
    user = await User.get_user_by_id(call.message.chat.id)
    user_profile = await user.get_user_profile()
    await call.message.edit_text(
        text=get_main_menu_page_text(),
    )
    await call.message.edit_reply_markup(
        reply_markup=get_main_menu_page_keyboard(
            config.connection_link,
            await user_profile.has_excursion(),
            await user_profile.has_knowledge_assesment()
        )
    )

@router.callback_query(GetUserDataPageCallbackData.filter())
async def start_collecting_user_data_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await call.message.delete()
    user_data = UserData(user_id=call.message.chat.id)
    user_data.last_message = await bot.send_message(
        chat_id=call.message.chat.id,
        text=get_get_user_name_full_name_surname_page_text()
    )
    await state.set_data({USER_DATA_ARGUMENT_NAME : user_data})
    await state.set_state(UserRegistrationFSM.name_full_name_surname)

@router.message(StateFilter(UserRegistrationFSM.name_full_name_surname))
async def get_user_name_full_name_surname_handler(message: Message, state: FSMContext, user_data: UserData) -> None:
    await message.delete()
    correct_value = True
    try:
        user_data.name_last_name_surname = message.text
    except ValueError:
        correct_value = False
    if correct_value:
        await state.set_state(UserRegistrationFSM.phone_number)
        await user_data.last_message.edit_text(
            text=get_get_user_phone_number_page_text()
        )
    else:
        await user_data.last_message.edit_text(
            text=get_get_user_name_full_name_surname_page_text()
        )

@router.message(StateFilter(UserRegistrationFSM.phone_number))
async def get_user_phone_number_handler(message: Message, bot: Bot, state: FSMContext, user_data: UserData,
                                        config: Config) -> None:
    await message.delete()
    correct_value = True
    try:
        user_data.phone_number = message.text
    except ValueError:
        correct_value = False
    if correct_value:
        await user_data.last_message.delete()
        user = await User.create_user(user_data)
        user_profile = await user.get_user_profile()
        await bot.send_message(
            chat_id=message.chat.id,
            text=get_main_menu_page_text(),
            reply_markup=get_main_menu_page_keyboard(
                config.connection_link,
                await user_profile.has_excursion(),
                await user_profile.has_knowledge_assesment()
            )
        )
        await state.clear()
    else:
        await user_data.last_message.edit_text(
            text=get_get_user_phone_number_page_text()
        )
