import asyncio

from sys import argv

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tg_bot.utils.inits import init_database
from tg_bot.utils.config import Config

from event_deleter import delete_outdated_events


async def main(dot_env_path: str):
    config = Config.load_config(dot_env_path)
    await init_database(config.database_path, config.models_path)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_outdated_events, 'interval', hours=1)
    scheduler.start()
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main(argv[-1]))
