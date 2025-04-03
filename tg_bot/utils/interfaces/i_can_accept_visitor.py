from __future__ import annotations
__all__ = ["ICanAcceptVisitor"]
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor


class ICanAcceptVisitor(ABC):
    @classmethod
    @abstractmethod
    async def accept(cls, visitor: IVisitor) -> None:
        pass