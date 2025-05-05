__all__ = ["EventEnum", "HandlerTypeEnum"]
from enum import IntEnum


class EventEnum(IntEnum):
    """Enumeration of event types in the system.

    This enum defines the different types of events that can be created and managed
    in the system. Each event type has a unique integer identifier.

    :cvar excursion: Represents an excursion event (ID: 1)
    :cvar knowledge_assesment: Represents a knowledge assessment event (ID: 2)
    """
    excursion = 1
    knowledge_assesment = 2

class HandlerTypeEnum(IntEnum):
    first_handler = 1
    get_info_handler = 2
    final_handler = 3
