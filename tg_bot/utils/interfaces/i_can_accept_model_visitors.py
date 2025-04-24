from __future__ import annotations
__all__ = ["ICanAcceptModelVisitors"]
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor


class ICanAcceptModelVisitors(ABC):
    """Interface for models that can accept model visitors.
    
    This interface defines the contract for models that can accept
    model visitors in the visitor design pattern. Classes implementing this
    interface must provide an accept method that takes a model visitor.
    """
    
    @classmethod
    @abstractmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accept a model visitor to perform operations.
        
        :param visitor: The model visitor object that will perform operations
        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError 