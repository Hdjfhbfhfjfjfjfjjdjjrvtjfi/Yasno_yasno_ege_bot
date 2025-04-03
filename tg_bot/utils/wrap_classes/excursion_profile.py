from __future__ import annotations
__all__ = ["ExcursionProfile"]
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tg_bot.models import Excursion


class ExcursionProfile:
    def __init__(self, excursion: Excursion):
        self.excursion = excursion