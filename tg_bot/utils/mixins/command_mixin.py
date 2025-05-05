__all__ = ["CommandMixin"]
from aiogram.types import BotCommand

from typing import Any

from tg_bot.utils.constants import COMMAND_ARGUMENT_NAME


class CommandMixin:
    data: dict[str, Any]

    @property
    def command(self) -> BotCommand:
        return self.data[COMMAND_ARGUMENT_NAME]