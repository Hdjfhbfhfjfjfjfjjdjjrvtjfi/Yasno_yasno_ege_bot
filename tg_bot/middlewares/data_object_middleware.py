__all__ = ["DataObjectMiddleware"]
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable, ClassVar


class DataObjectMiddleware(BaseMiddleware):
    """Middleware for managing data objects in the FSM context.
    
    This middleware is responsible for injecting data objects from the FSM state
    into the handler's data dictionary.

    :cvar STATE_STRING: String constant representing the state key in the data dictionary
    :ivar data_object_name: The name of the data object to inject
    """
    STATE_STRING: ClassVar[str] = "state"
    def __init__(self, data_object_name: str):
        """Initializes the middleware with the specified data object name.
        
        :param data_object_name: The name of the data object to inject into the handler's data
        """
        self.data_object_name = data_object_name

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        """Processes the incoming event and injects the data object if present in the state.
        
        :param handler: The handler function to be called
        :param event: The incoming Telegram event
        :param data: The data dictionary to be passed to the handler
        :return: The result of the handler execution
        """
        state: FSMContext = data[self.STATE_STRING]
        state_data = await state.get_data()
        if self.data_object_name in state_data.keys():
            data[self.data_object_name] = state_data[self.data_object_name]
        return await handler(event, data)