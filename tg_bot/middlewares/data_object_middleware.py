__all__ = ["DataObjectMiddleware"]
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject


class DataObjectMiddleware(BaseMiddleware):
    STATE_STRING: str = "state"
    def __init__(self, data_object_name: str):
        self.data_object_name: str = data_object_name

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        state: FSMContext = data[self.STATE_STRING]
        state_data = await state.get_data()
        if self.data_object_name in state_data.keys():
            data[self.data_object_name] = state_data[self.data_object_name]
        return await handler(event, data)