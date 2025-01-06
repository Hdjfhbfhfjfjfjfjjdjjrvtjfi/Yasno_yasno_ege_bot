__all__ = ["Config"]
from dataclasses import dataclass


@dataclass
class Config:
    token: str
    database_path: str
    models_path: str
