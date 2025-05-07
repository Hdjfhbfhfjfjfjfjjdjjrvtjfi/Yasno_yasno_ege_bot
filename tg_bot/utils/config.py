__all__ = ["Config"]
from dataclasses import dataclass

from environs import Env


@dataclass(frozen=True)
class Config:
    """
    Configuration class for the bot application.

    This class holds all the configuration settings required for the bot to operate.
    It is implemented as a frozen dataclass to ensure immutability of configuration values.
    The configuration is loaded from environment variables using the environs package.
    :ivar token: Telegram bot token for API authentication
    :ivar database_path: Path to the SQLite database file
    :ivar models_path: Path to the module containing Tortoise ORM models
    :ivar agreement_on_data_processing_link: URL to the data processing agreement
    :ivar connection_link: URL for connecting to the bot owner
    :ivar bot_link: URL of the bot
    :ivar max_count_of_excursion_visitors: Maximum number of visitors allowed per excursion
    :ivar cluster_size: Size of data clusters for pagination
    :ivar yookassa_account_id: YooKassa payment system account ID
    :ivar yookassa_secret_key: YooKassa payment system API secret key
    """

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
    first_guide_image_path: str
    second_guide_image_path: str
    excursion_image_path: str

    @classmethod
    def load_config(cls, dot_env_path: str) -> "Config":
        """Loads configuration from a .env file.

        This class method reads environment variables from the specified .env file
        and creates a new Config instance with the loaded values.
        e
        :param dot_env_path: Path to the .env file containing configuration values
        :return: A new Config instance with values loaded from the .env file
        :raise environs.EnvError: If required environment variables are missing or invalid
        """
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
            first_guide_image_path=env.str("FIRST_GUIDE_IMAGE_PATH"),
            second_guide_image_path=env.str("SECOND_GUIDE_IMAGE_PATH"),
            excursion_image_path=env.str("EXCURSION_IMAGE_PATH"),
        )
