__all__ = ["TextMessageBuilder"]
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup

from typing import ClassVar, Awaitable, Any, Callable

from tg_bot.utils.interfaces import IMessageBuilder


class TextMessageBuilder(IMessageBuilder):
    __CREATE_KEY: ClassVar[object] = object()

    def __init__(self, create_key: object, message: Awaitable[Message]) -> None:
        if create_key is not self.__CREATE_KEY:
            raise Exception("Class can't be instantiated by constructor")
        self._initial_message_coroutine: Awaitable[Message] = message
        self._changes: list[tuple[Callable[[Any, ...], Awaitable[Any]], dict[str, Any]]] = []

    @staticmethod
    async def __wrap_coroutine(message: Message) -> Message:
        return message

    @classmethod
    def create_from_existing_message(cls, message: Message) -> "TextMessageBuilder":
        return cls(cls.__CREATE_KEY, cls.__wrap_coroutine(message))

    @classmethod
    def send_new_message(cls, text: str, bot: Bot, chat_id: int) -> "TextMessageBuilder":
        return cls(cls.__CREATE_KEY, bot.send_message(chat_id=chat_id, text=text))

    def edit_reply_markup(self, reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> "TextMessageBuilder":
        self._changes.append((Message.edit_reply_markup, {"reply_markup" : reply_markup}))
        return self

    def edit_text(self, text: str) -> "TextMessageBuilder":
        self._changes.append((Message.edit_text, {"text" : text}))
        return self

    async def send(self) -> Message:
        message: Message = await self._initial_message_coroutine
        for change in self._changes:
            await change[0](message, **change[1])
        return message
