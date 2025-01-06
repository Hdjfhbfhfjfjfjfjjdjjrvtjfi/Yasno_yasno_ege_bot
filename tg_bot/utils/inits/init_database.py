__all__ = ["init_database"]
from tortoise import Tortoise


async def init_database(db_path: str, models_path: str):
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={'models': [models_path]},
    )
    await Tortoise.generate_schemas()