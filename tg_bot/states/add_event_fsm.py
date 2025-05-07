__all__ = ["AddEventFSM"]
from aiogram.fsm.state import State, StatesGroup


class AddEventFSM(StatesGroup):
    """Finite State Machine for managing the event creation process.
    
    :ivar year: State for collecting the year of the event
    :ivar month: State for collecting the month of the event
    :ivar day: State for collecting the day of the event
    :ivar hour: State for collecting the hour of the event
    :ivar minute: State for collecting the minute of the event
    :ivar max_count_of_buyings: State for collecting the maximum number of attendees
    :ivar price: State for collecting the price of the event
    :ivar string_field: State for collecting additional string information
    """
    year = State()
    month = State()
    day = State()
    hour = State()
    minute = State()
    max_count_of_buyings = State()
    price = State()
    string_field = State()