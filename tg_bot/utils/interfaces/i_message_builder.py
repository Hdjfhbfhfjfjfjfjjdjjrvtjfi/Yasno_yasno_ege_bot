__all__ = ["IMessageBuilder"]
from abc import ABC, abstractmethod

from typing import ClassVar

from aiogram.types import Message


class IMessageBuilder(ABC):
    @abstractmethod
    async def send(self) -> Message:
        raise NotImplementedError

