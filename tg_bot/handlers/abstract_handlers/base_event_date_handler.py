from aiogram.filters.callback_data import CallbackData

from typing import Tuple, TypeVar

from datetime import datetime

from typing_extensions import Generic

from tg_bot.handlers.abstract_handlers import BaseEventHandler
from tg_bot.utils.enums import EventEnum
from tg_bot.utils.texts import (
    get_choose_excursion_date_page_text,
    get_choose_knowledge_assesment_date_page_text
)

T = TypeVar('T', bound=CallbackData)

class BaseEventDateHandler(Generic[T], BaseEventHandler[T]):
    """Base class for event date selection handlers."""
    
    async def get_events_data(self, page_index: int) -> Tuple[Tuple, int]:
        """Get events data for the specified page."""
        events, count_of_clusters = await self.event_model.get_cluster_and_count_of_clusters_by_date(
            datetime.now(),
            page_index,
            self.config.cluster_size
        )
        data = tuple([
            (event.id, event.date, (await event.get_count_of_buyings()) < event.max_count_of_buyings)
            for event in events
        ])
        return data, count_of_clusters

    def get_text(self) -> str:
        """Get the text for the event date page."""
        return (get_choose_excursion_date_page_text() 
                if self.unpacked_callback_data.event == EventEnum.excursion 
                else get_choose_knowledge_assesment_date_page_text()) 