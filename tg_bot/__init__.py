__all__ = ["Config", "routers", "init_database", "init_yookassa_api"]
from tg_bot.utils.config import Config
from tg_bot.utils.inits import init_database, init_yookassa_api
from tg_bot.handlers import routers
