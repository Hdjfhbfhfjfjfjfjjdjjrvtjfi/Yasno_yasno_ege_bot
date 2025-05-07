__all__ = ["delete_outdated_knowledge_assesments"]
from datetime import datetime

from tg_bot.models import KnowledgeAssesment, BotUserProfile


async def delete_outdated_knowledge_assesments(date: datetime):
    outdated_knowledge_assesments = await KnowledgeAssesment.get_outdated_events(date)
    for knowledge_assesment in outdated_knowledge_assesments:
        profiles: list[BotUserProfile] = await knowledge_assesment.bot_user_profiles.all()
        for profile in profiles:
            await profile.delete_test_result()
        await knowledge_assesment.bot_user_profiles.clear()
        await knowledge_assesment.delete()
