__all__ = ["CombinedModelAndABCMeta"]
from tortoise.models import ModelMeta

from abc import ABCMeta


class CombinedModelAndABCMeta(ABCMeta, ModelMeta):
    pass
