from asyncio import run

from aiogram import Bot, Dispatcher

from sys import argv

from tg_bot import Config, init_database, init_yookassa_api, routers


async def main(dot_env_path: str):
    config: Config = Config.load_config(dot_env_path)
    await init_database(config.database_path, config.models_path)
    init_yookassa_api(config.yookassa_account_id, config.yookassa_secret_key)
    bot: Bot = Bot(token=config.token)
    dp: Dispatcher = Dispatcher(config=config)
    dp.include_routers(*routers)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main(argv[-1]))

