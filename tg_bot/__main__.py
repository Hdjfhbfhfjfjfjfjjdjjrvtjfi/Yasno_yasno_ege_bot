from asyncio import run

from aiogram import Bot, Dispatcher

from sys import argv

from tg_bot import Config, load_config, init_database


async def main(dot_env_path: str):
    config: Config = load_config(dot_env_path)
    await init_database(config.database_path, config.models_path)
    bot: Bot = Bot(token=config.token)
    dp: Dispatcher = Dispatcher(config=config)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main(argv[-1]))

