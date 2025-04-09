__all__ = ["CombinedModelAndABCMeta"]
from abc import ABCMeta

from tortoise.models import ModelMeta


class CombinedModelAndABCMeta(ABCMeta, ModelMeta):
    pass
