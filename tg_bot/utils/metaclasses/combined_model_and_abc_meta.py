__all__ = ["CombinedModelAndABCMeta"]
from abc import ABCMeta

from tortoise.models import ModelMeta


class CombinedModelAndABCMeta(ABCMeta, ModelMeta):
    """A metaclass that combines the functionality of ABCMeta and ModelMeta.

    This metaclass allows a class to be both an abstract base class (ABC) and a Tortoise ORM model.
    It inherits from both ABCMeta (for abstract class functionality) and ModelMeta (for ORM functionality).

    This enables the creation of abstract base classes that can also serve as ORM models,
    allowing for shared functionality and structure across different model implementations.
    """
    pass
