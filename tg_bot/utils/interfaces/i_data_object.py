__all__ = ["IDataObject"]
from aiogram.types import Message

from abc import ABC, abstractmethod


class IDataObject(ABC):

    last_message: Message | None = None

    @abstractmethod
    async def create_model_instance(self) -> None:
        raise NotImplementedError