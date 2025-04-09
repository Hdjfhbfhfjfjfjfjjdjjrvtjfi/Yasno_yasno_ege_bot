__all__ = ["Config"]
from dataclasses import dataclass

from environs import Env


@dataclass(frozen=True)
class Config:
    token: str
    database_path: str
    models_path: str
    agreement_on_data_processing_link: str
    connection_link: str
    bot_link: str
    max_count_of_excursion_visitors: int
    cluster_size: int
    yookassa_account_id: str
    yookassa_secret_key: str

    @classmethod
    def load_config(cls, dot_env_path: str) -> "Config":
        env: Env = Env()
        env.read_env(dot_env_path)
        return cls(
            token=env.str("TOKEN"),
            database_path=env.str("DATABASE_PATH"),
            models_path=env.str("MODELS_PATH"),
            agreement_on_data_processing_link=env.str("AGREEMENT_ON_DATA_PROCESSING_LINK"),
            connection_link=env.str("CONNECTION_LINK"),
            max_count_of_excursion_visitors=env.int("MAX_COUNT_OF_EXCURSION_VISITORS"),
            cluster_size=env.int("CLUSTER_SIZE"),
            yookassa_account_id=env.str("YOOKASSA_ACCOUNT_ID"),
            yookassa_secret_key=env.str("YOOKASSA_SECRET_KEY"),
            bot_link=env.str("BOT_LINK"),
        )
