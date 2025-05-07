__all__ = ["CheckAdministratorRightsMiddleware"]
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from typing import Callable, Dict, Any, Awaitable

from tg_bot.models import Administrator


class CheckAdministratorRightsMiddleware(BaseMiddleware):
    """Middleware for checking administrator rights.
    
    This middleware verifies if the user has administrator rights before allowing
    the handler to process the event. If the user is not an administrator,
    the event is deleted.
    """
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject | Message | CallbackQuery, data: Dict[str, Any]) -> Any:
        """Processes the incoming event and checks administrator rights.
        
        :param handler: The handler function to be called
        :param event: The incoming Telegram event (Message or CallbackQuery)
        :param data: The data dictionary to be passed to the handler
        :return: The result of the handler execution if user is an administrator, None otherwise
        """
        if await Administrator.get_administrator_by_id(event.chat.id) is not None:
            return await handler(event, data)
        else:
            await event.delete()

