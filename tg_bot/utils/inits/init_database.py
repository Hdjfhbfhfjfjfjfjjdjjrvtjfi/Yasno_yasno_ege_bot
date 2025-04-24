__all__ = ["init_database"]
from tortoise import Tortoise


async def init_database(db_path: str, models_path: str) -> None:
    """Initialize the database connection and generate schemas.

    :param db_path: Path to the SQLite database file
    :param models_path: Path to the module containing Tortoise ORM models
    :return: None
    """
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={'models': [models_path]},
    )
    await Tortoise.generate_schemas()
