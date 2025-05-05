__all__ = ["ConfigMixin"]
from typing import Any

from tg_bot.utils.constants import CONFIG_ARGUMENT_NAME


class ConfigMixin:
    data: dict[str, Any]

    @property
    def config(self):
        return self.data[CONFIG_ARGUMENT_NAME]