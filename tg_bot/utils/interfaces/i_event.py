__all__ = ["IEvent"]
from abc import ABC, abstractmethod

from datetime import datetime

from typing import Self, Any

from tortoise.contrib.mysql.fields import UUIDField
from tortoise.fields import IntField


class IEvent(ABC):

    id: UUIDField
    _year: IntField
    _month: IntField
    _day: IntField
    _hour: IntField
    _minute: IntField
    price: IntField
    max_count_of_buyings: IntField

    @abstractmethod
    def get_pay_text_args(self) -> list[Any]:
        raise NotImplementedError

    @property
    def date(self) -> datetime:
        raise NotImplementedError

    @date.setter
    def date(self, value: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_count_of_buyings(self) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_by_id(cls, event_id: str) -> Self | None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_cluster_and_count_of_clusters_by_date(cls, date: datetime, cluster_index: int,
                                                        cluster_size: int) -> tuple[tuple[Self, ...], int]:
        raise NotImplementedError