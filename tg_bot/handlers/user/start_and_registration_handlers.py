__all__ = ["router"]
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram.types import TelegramObject

from tg_bot.handlers.abstract_handlers import FormBaseHandler
from tg_bot.models import User
from tg_bot.filters.callback_data import GetUserDataPageCallbackData, MainMenuPageCallbackData
from tg_bot.utils.enums import HandlerTypeEnum
from tg_bot.utils.message_builders import TextMessageBuilder
from tg_bot.utils.mixins import ConfigMixin
from tg_bot.utils.texts import (
    agreement_on_data_processing_page_text,
    get_main_menu_page_text,
    get_get_user_name_full_name_surname_page_text,
    get_get_user_phone_number_page_text
)
from tg_bot.utils.data_objects import UserData
from tg_bot.states import UserRegistrationFSM
from tg_bot.keyboards import agreement_on_data_processing_page_keyboard, get_main_menu_page_keyboard
from tg_bot.utils.constants import USER_DATA_ARGUMENT_NAME
from tg_bot.utils.validators import full_name_validator, phone_number_validator

router: Router = Router()

@router.message(CommandStart())
class StartHandler(MessageHandler, ConfigMixin):
    """Handler for the /start command.
    
    This handler manages the initial interaction with users when they start the bot.
    It checks if the user is new or returning and provides appropriate responses.
    """

    async def handle(self) -> None:
        """Handle the /start command.
        
        If the user is new, shows the data processing agreement.
        If the user is returning, shows the main menu.
        """
        await self.event.delete()
        user = await User.get_user_by_id(self.event.from_user.id)
        if user is None:
            await self.bot.send_message(
                chat_id=self.event.chat.id,
                text=agreement_on_data_processing_page_text(),
                reply_markup=agreement_on_data_processing_page_keyboard(
                    self.config.agreement_on_data_processing_link
                ),
            )
        else:
            user_profile = await user.get_user_profile()
            await self.bot.send_message(
                chat_id=self.event.chat.id,
                text=get_main_menu_page_text(),
                reply_markup=get_main_menu_page_keyboard(
                    self.config.connection_link,
                    await user_profile.has_excursion(),
                    await user_profile.has_knowledge_assesment()
                )
            )


@router.callback_query(MainMenuPageCallbackData.filter())
class MainMenuHandler(CallbackQueryHandler, ConfigMixin):
    """Handler for the main menu navigation.
    
    This handler manages the main menu interactions and updates the menu display.
    """
    
    async def handle(self) -> None:
        """Handle main menu navigation.
        
        Updates the main menu text and keyboard based on the user's current state.
        """
        user = await User.get_user_by_id(self.event.message.chat.id)
        user_profile = await user.get_user_profile()
        await self.event.message.delete()
        await self.bot.send_message(
            chat_id=self.event.message.chat.id,
            text=get_main_menu_page_text(),
            reply_markup=get_main_menu_page_keyboard(
                self.config.connection_link,
                await user_profile.has_excursion(),
                await user_profile.has_knowledge_assesment()
            )
        )


@router.callback_query(GetUserDataPageCallbackData.filter())
class StartCollectingUserDataHandler(FormBaseHandler[UserData]):
    """Handler for starting the user data collection process.
    
    This handler initiates the user registration process by collecting
    the user's personal information.
    """
    
    async def handle(self) -> None:
        """Start collecting user data.
        
        Deletes the previous message and initiates the name collection process.
        """
        await self.initialize_form_data(
            UserData(user_id=self.event.message.chat.id),
            TextMessageBuilder.send_new_message(
                get_get_user_name_full_name_surname_page_text(),
                self.bot,
                self.event.message.chat.id
            ),UserRegistrationFSM.name_full_name_surname,
            USER_DATA_ARGUMENT_NAME
        )

@router.message(StateFilter(UserRegistrationFSM.name_full_name_surname))
class GetUserNameHandler(FormBaseHandler[UserData]):
    """Handler for collecting the user's full name.
    
    This handler validates and processes the user's full name input.
    """

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = USER_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self) -> None:
        """Handle the user's full name input.
        
        Validates the name and proceeds to phone number collection if valid.
        """
        self.data_object.name_last_name_surname = await self.process_text_state(
            UserRegistrationFSM.phone_number,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_user_phone_number_page_text()),
            [full_name_validator]
        )


@router.message(StateFilter(UserRegistrationFSM.phone_number))
class GetUserPhoneNumberHandler(FormBaseHandler[UserData], ConfigMixin, handler_type=HandlerTypeEnum.final_handler):
    """Handler for collecting the user's phone number.
    
    This handler validates and processes the user's phone number input.
    """

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = USER_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)
    
    async def handle(self) -> None:
        """Handle the user's phone number input.
        
        Validates the phone number and completes the registration process if valid.
        """
        self.data_object.phone_number = await self.process_text_state(
            UserRegistrationFSM.phone_number,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message),
            [phone_number_validator]
        )
        if self.data_object.phone_number is not None:
            await self.data_object.create_model_instance()
            user = await User.get_user_by_id(self.event.chat.id)
            user_profile = await user.get_user_profile()
            await self.bot.send_message(
                chat_id=self.event.chat.id,
                text=get_main_menu_page_text(),
                reply_markup=get_main_menu_page_keyboard(
                    self.config.connection_link,
                    await user_profile.has_excursion(),
                    await user_profile.has_knowledge_assesment()
                )
            )
