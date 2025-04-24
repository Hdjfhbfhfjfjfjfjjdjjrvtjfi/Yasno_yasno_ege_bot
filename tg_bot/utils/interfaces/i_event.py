from __future__ import annotations
__all__ = ["IEvent"]
from abc import ABC, abstractmethod

from datetime import datetime

from typing import Self, Any, TYPE_CHECKING

from tortoise.contrib.mysql.fields import UUIDField
from tortoise.fields import IntField

if TYPE_CHECKING:
    from tg_bot.utils.data_objects import  EventData


class IEvent(ABC):
    """
    Abstract base class defining the interface for event models in the system.
    This interface provides a contract for event-related operations and data management.
    All event implementations must inherit from this class and implement its abstract methods.

    :ivar id: Unique identifier for the event
    :ivar _year: Year component of the event date
    :ivar _month: Month component of the event date
    :ivar _day: Day component of the event date
    :ivar _hour: Hour component of the event time
    :ivar _minute: Minute component of the event time
    :ivar price: Price of the event
    :ivar max_count_of_buyings: Maximum number of purchases allowed for this event
    """

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
        """Retrieves arguments needed for generating payment text.

        :return: List of arguments required for payment text generation
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @property
    def date(self) -> datetime:
        """Gets the event date and time.

        :return: The event date and time as a datetime object
        """
        raise NotImplementedError

    @date.setter
    def date(self, value: datetime) -> None:
        """Sets the event date and time.

        :param value: The new date and time to set
        :return: None
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_outdated_events(cls, date: datetime) -> list[Self]:
        """Retrieves all events that are outdated based on the given date.

        :param date: The reference date to check against
        :return: List of outdated events
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def get_count_of_buyings(self) -> int:
        """Gets the current number of purchases for this event.

        :return: The number of purchases made for this event
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_by_id(cls, event_id: str) -> Self | None:
        """Retrieves an event by its ID.

        :param event_id: The ID of the event to retrieve
        :return: The event if found, None otherwise
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create_event(cls, event_data: EventData) -> Self:
        """Creates a new event from the provided data.

        :param event_data: The data to create the event from
        :return: The newly created event
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_cluster_and_count_of_clusters_by_date(cls, date: datetime, cluster_index: int,
                                                      cluster_size: int) -> tuple[tuple[Self, ...], int]:
        """Retrieves a cluster of events and the total number of clusters for a given date.

        :param date: The date to get events for
        :param cluster_index: The index of the cluster to retrieve
        :param cluster_size: The size of each cluster
        :return: A tuple containing the cluster of events and the total number of clusters
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError