__all__ = ["StateMixin"]
from typing import Any

from aiogram.fsm.context import FSMContext

from tg_bot.utils.constants import STATE_CONTEXT_ARGUMENT_NAME

class StateMixin:
    data: dict[str, Any]

    @property
    def state(self) -> FSMContext:
        return self.data[STATE_CONTEXT_ARGUMENT_NAME]