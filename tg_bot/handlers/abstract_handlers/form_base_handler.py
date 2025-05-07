__all__ = ["FormBaseHandler"]
from aiogram.handlers import BaseHandler, CallbackQueryHandler
from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.fsm.state import State

from typing import TypeVar, Generic, ClassVar, Any, Callable

from tg_bot.utils.interfaces import IDataObject, IMessageBuilder
from tg_bot.utils.mixins import DataObjectMixin, StateMixin
from tg_bot.utils.enums import HandlerTypeEnum


T = TypeVar('T', bound=IDataObject)
K = TypeVar('K')

class FormBaseHandler(Generic[T], BaseHandler[Message | CallbackQuery], DataObjectMixin[T], StateMixin):
    handler_type: ClassVar[HandlerTypeEnum] = HandlerTypeEnum.get_info_handler

    def __init_subclass__(cls, **kwargs):
        external_type: HandlerTypeEnum = kwargs.get("handler_type")
        if external_type is not None:
            cls.handler_type = external_type

    @property
    def callback_data(self) -> str:
        return self.event.data

    async def handle(self) -> Any:
        raise NotImplementedError

    async def initialize_form_data(self, data_object: T, message_builder: IMessageBuilder, first_state: State,
                                   data_object_argument_name: str, command: BotCommand | None = None) -> None:
        if isinstance(self.event, Message):
            await self.event.delete()
        else:
            await self.event.message.delete()
        self._data_object_argument_name = data_object_argument_name
        self.data_object = data_object
        if command is not None:
            await self._process_command(command)
        self.data_object.last_message = await message_builder.send()
        await self.state.set_state(first_state)
        await self.state.set_data({data_object_argument_name: self.data_object})

    async def process_text_state(self, next_state: State, message_builder: IMessageBuilder,
                                 validators: list[Callable[[str], bool]] | None = None) -> str | None:
        result = await self._process_input_data(validators)
        if (result is not None and validators is not None and
            not self._process_data_through_validators(result, validators)):
            result = None
        if result is not None:
            await self._send_message(message_builder, next_state)
        return result

    async def process_numeric_state(self, next_state: State, message_builder: IMessageBuilder,
                                    validators: list[Callable[[int], bool]] | None = None) -> int | None:
        result = await self._process_input_data(validators)
        if result is not None and result.isdigit():
            result = int(result)
            if validators is not None and not self._process_data_through_validators(result ,validators):
                    result = None
        else:
            result = None
        if result is not None:
            await self._send_message(message_builder, next_state)
        return result

    async def _send_message(self, message_builder, next_state) -> None:
        if self.handler_type == HandlerTypeEnum.get_info_handler:
            await message_builder.send()
            await self.state.set_state(next_state)
        elif self.handler_type == HandlerTypeEnum.final_handler:
            await self.data_object.last_message.delete()
            await self.state.clear()

    async def _process_input_data(self, validators: list[Callable[[str], bool]] | None = None) -> str | None:
        if isinstance(self.event, Message):
            result = await self._process_text()
        else:
            result = str(await self._process_callback_data())
        if result is not None and validators is not None:
            if not self._process_data_through_validators(result, validators):
                result = None
        return result

    @staticmethod
    def _process_data_through_validators[K](value: K, validators: list[Callable[[K], bool]]) -> bool:
        for validator in validators:
            if not validator(value):
                return False
        return True

    async def _process_text(self) -> str | None:
        await self.event.delete()
        result: str | None = None
        if self.event.text is not None:
            result = self.event.text
        elif self.event.caption is not None:
            result = self.event.caption
        return result

    async def _process_command(self, command: BotCommand) -> None:
        pass

    async def _process_callback_data(self) -> str | None:
        raise NotImplementedError
