from asyncio import run

import warnings

from aiogram import Bot, Dispatcher

from sys import argv

from tg_bot import Config, init_database, init_yookassa_api, routers


async def main(dot_env_path: str):
    """Main function to run the bot.
    
    :param dot_env_path: Path to the .env file containing the bot configuration
    """
    warnings.filterwarnings("ignore")
    config: Config = Config.load_config(dot_env_path)
    await init_database(config.database_path, config.models_path)
    init_yookassa_api(config.yookassa_account_id, config.yookassa_secret_key)
    bot: Bot = Bot(token=config.token)
    dp: Dispatcher = Dispatcher(config=config)
    dp.include_routers(*routers)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main(argv[-1]))

