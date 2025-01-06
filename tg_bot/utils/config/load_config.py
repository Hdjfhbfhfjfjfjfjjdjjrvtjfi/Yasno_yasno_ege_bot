__all__ = ["load_config"]
from environs import Env

from tg_bot.utils.config import Config


def load_config(dot_env_path: str) -> Config:
    env: Env = Env()
    env.read_env(dot_env_path)
    return Config(
        token=env.str("TOKEN"),
        database_path=env.str("DATABASE_PATH"),
        models_path=env.str("MODELS_PATH"),
    )
