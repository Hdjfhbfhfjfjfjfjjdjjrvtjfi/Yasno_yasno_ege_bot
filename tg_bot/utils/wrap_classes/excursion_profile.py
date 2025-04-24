from __future__ import annotations
__all__ = ["ExcursionProfile"]
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tg_bot.models import Excursion


class ExcursionProfile:
    """
    A wrapper class for excursion data.
    
    This class serves as a container for excursion information,
    providing a clean interface to access and manipulate excursion data.

    :cvar excursion: The wrapped excursion object
    """

    def __init__(self, excursion: Excursion) -> None:
        """
        Initializes a new ExcursionProfile instance.
        
        :param excursion: The excursion object to wrap
        :return: None
        """
        self.excursion: Excursion = excursion