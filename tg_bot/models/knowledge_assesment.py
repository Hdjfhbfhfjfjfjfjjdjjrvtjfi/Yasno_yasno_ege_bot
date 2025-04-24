from __future__ import annotations
__all__ = ["KnowledgeAssesment"]
from tortoise import Model
from tortoise.fields import UUIDField, TextField, IntField, ManyToManyRelation

from datetime import datetime

from typing import Any, TYPE_CHECKING, Optional

from tg_bot.utils.mixins import ClusterFetcherMixin
from tg_bot.utils.interfaces import IEvent, ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.interfaces import IModelVisitor
    from tg_bot.utils.data_objects import EventData


class KnowledgeAssesment(Model, IEvent, ClusterFetcherMixin, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a knowledge assessment event in the system.

    :ivar id: UUID primary key field for the assessment
    :ivar _year: Integer field for the year of the assessment
    :ivar _month: Integer field for the month of the assessment
    :ivar _day: Integer field for the day of the assessment
    :ivar _hour: Integer field for the hour of the assessment
    :ivar _minute: Integer field for the minute of the assessment
    :ivar max_count_of_buyings: Maximum number of participants allowed
    :ivar price: Price of the assessment
    :ivar webinar_link: Text field containing the webinar link
    :ivar bot_user_profiles: Many-to-many relationship with BotUserProfile model
    """
    id = UUIDField(pk=True, unique=True)
    _year = IntField(default=datetime.now().year)
    _month = IntField(default=datetime.now().month)
    _day = IntField(default=datetime.now().day)
    _hour = IntField(default=datetime.now().hour)
    _minute = IntField(default=datetime.now().minute)
    max_count_of_buyings = IntField()
    price = IntField()
    webinar_link = TextField()
    bot_user_profiles: ManyToManyRelation

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the knowledge assessment visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_knowledge_assesment()

    @property
    def date(self) -> datetime:
        """Gets the complete datetime of the knowledge assessment.
        
        :return: Datetime object representing the assessment's date and time
        """
        return datetime(self._year, self._month, self._day, self._hour, self._minute)

    @date.setter
    def date(self, value: datetime) -> None:
        """Sets the date and time components of the knowledge assessment.
        
        :param value: Datetime object containing the new date and time
        :return: None
        """
        self._year = value.year
        self._month = value.month
        self._day = value.day
        self._hour = value.hour
        self._minute = value.minute

    @classmethod
    async def get_outdated_events(cls, date: datetime) -> list["KnowledgeAssesment"]:
        """Retrieves all knowledge assessments that have already occurred before the given date.
        
        :param date: The reference date to compare against
        :return: List of outdated KnowledgeAssesment instances
        """
        return (await cls.filter(_year__lt=date.year) +
                await cls.filter(_year=date.year).filter(_month__lt=date.month) +
                await cls.filter(_year=date.year).filter(_month=date.month).filter(_day__lt=date.day))

    def get_pay_text_args(self) -> list[Any]:
        """Gets the arguments needed for payment text formatting.
        
        :return: List containing the assessment's date and webinar link
        """
        return [self.date, self.webinar_link]

    async def get_count_of_buyings(self) -> int:
        """Returns the count of users that have purchased this knowledge assessment.
        
        :return: Number of users who have bought this assessment
        """
        return await self.bot_user_profiles.all().count()

    @classmethod
    async def create_event(cls, event_data: EventData) -> "KnowledgeAssesment":
        """Creates a new knowledge assessment event from the provided data.
        
        :param event_data: EventData object containing the assessment details
        :return: The newly created KnowledgeAssesment instance
        """
        knowledge_assesment = await cls.create(
            webinar_link=event_data.string_field,
            price=event_data.price,
            max_count_of_buyings=event_data.max_count_of_buyings
        )
        knowledge_assesment.date = datetime(
            event_data.year,
            event_data.month,
            event_data.day,
            event_data.hour,
            event_data.minute
        )
        await knowledge_assesment.save()
        return knowledge_assesment

    @classmethod
    async def get_by_id(cls, event_id: str) -> Optional["KnowledgeAssesment"]:
        """Retrieves a knowledge assessment by its ID.
        
        :param event_id: The UUID of the assessment to retrieve
        :return: The KnowledgeAssesment instance if found, None otherwise
        """
        return await cls.get_or_none(id=event_id)

    @classmethod
    async def get_cluster_and_count_of_clusters_by_date(cls, date: datetime, cluster_index: int, cluster_size: int
                                                        ) -> tuple[tuple["KnowledgeAssesment", ...], int]:
        """Retrieves a cluster of knowledge assessments and the total number of clusters.
        
        :param date: The reference date for filtering assessments
        :param cluster_index: The index of the cluster to retrieve
        :param cluster_size: The size of each cluster
        :return: Tuple containing the cluster of assessments and total cluster count
        """
        query_set = cls.filter(_year__gte=date.year).filter(_month__gte=date.month)
        return await cls._get_cluster_of_items_and_count_of_clusters(query_set, cluster_index, cluster_size)
