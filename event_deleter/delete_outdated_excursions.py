__all__ = ["delete_outdated_excursions"]
from datetime import datetime

from tg_bot.models import Excursion


async def delete_outdated_excursions(date: datetime):
    outdated_excursions = await Excursion.get_outdated_events(date)
    for excursion in outdated_excursions:
        await excursion.bot_user_profiles.clear()
        await excursion.delete()
