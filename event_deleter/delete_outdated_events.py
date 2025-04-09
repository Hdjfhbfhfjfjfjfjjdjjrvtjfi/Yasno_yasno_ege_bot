__all__ = ["delete_outdated_events"]
from datetime import datetime

from event_deleter import delete_outdated_excursions, delete_outdated_knowledge_assesments

async def delete_outdated_events():
    date = datetime.now()
    await delete_outdated_excursions(date)
    await delete_outdated_knowledge_assesments(date)