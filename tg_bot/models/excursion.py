from __future__ import annotations
__all__ = ["Excursion"]
from tortoise import Model, BaseDBAsyncClient
from tortoise.fields import UUIDField, TextField, ManyToManyRelation, IntField

from datetime import datetime

from typing import Any, TYPE_CHECKING, Optional

from tg_bot.utils.mixins import ClusterFetcherMixin
from tg_bot.utils.interfaces import IEvent, ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IVisitor
    from tg_bot.utils.data_objects import EventData


class Excursion(Model, ClusterFetcherMixin, IEvent, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    id = UUIDField(pk=True, unique=True)
    _year = IntField(default=datetime.now().year)
    _month = IntField(default=datetime.now().month)
    _day = IntField(default=datetime.now().day)
    _hour = IntField(default=datetime.now().hour)
    _minute = IntField(default=datetime.now().minute)
    max_count_of_buyings = IntField()
    price = IntField()
    address = TextField()
    bot_user_profiles: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_excursion()

    async def delete(self, using_db: BaseDBAsyncClient | None = None) -> None:
        await self.bot_user_profiles.clear()
        await super().delete(using_db=using_db)

    @property
    def date(self) -> datetime:
        return datetime(self._year, self._month, self._day, self._hour, self._minute)

    @date.setter
    def date(self, value: datetime) -> None:
        self._year = value.year
        self._month = value.month
        self._day = value.day
        self._hour = value.hour
        self._minute = value.minute

    @classmethod
    async def get_outdated_events(cls, date: datetime) -> list["Excursion"]:
        return (await cls.filter(_year__lt=date.year) +
                await cls.filter(_year=date.year).filter(_month__lt=date.month) +
                await cls.filter(_year=date.year).filter(_month=date.month).filter(_day__lt=date.day))

    def get_pay_text_args(self) -> list[Any]:
            return [self.date, self.address]

    async def get_count_of_buyings(self) -> int:
        return await self.bot_user_profiles.all().count()

    @classmethod
    async def create_event(cls, event_data: EventData) -> "Excursion":
        excursion = await cls.create(
            address=event_data.string_field,
            price=event_data.price,
            max_count_of_buyings=event_data.max_count_of_buyings
        )
        excursion.date = datetime(
            event_data.year,
            event_data.month,
            event_data.day,
            event_data.hour,
            event_data.minute
        )
        await excursion.save()
        return excursion

    @classmethod
    async def get_by_id(cls, event_id: str) -> Optional["Excursion"]:
        return await cls.get_or_none(id=event_id)

    @classmethod
    async def get_cluster_and_count_of_clusters_by_date(cls, date: datetime, cluster_index: int, cluster_size: int
                                                        ) -> tuple[tuple["Excursion", ...], int]:
        query_set = cls.filter(_year__gte=date.year).filter(_month__gte=date.month)
        return await cls._get_cluster_of_items_and_count_of_clusters(query_set, cluster_index, cluster_size)
