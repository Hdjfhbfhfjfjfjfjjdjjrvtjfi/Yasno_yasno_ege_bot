__all__ = ["CheckAdministratorRightsMiddleware"]
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from typing import Callable, Dict, Any, Awaitable

from tg_bot.models import Administrator


class CheckAdministratorRightsMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject | Message | CallbackQuery, data: Dict[str, Any]) -> Any:
        if await Administrator.get_administrator_by_id(event.chat.id) is not None:
            return await handler(event, data)
        else:
            await event.delete()

