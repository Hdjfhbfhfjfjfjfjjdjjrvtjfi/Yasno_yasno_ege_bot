__all__ = ["AddEventFSM"]
from aiogram.fsm.state import State, StatesGroup


class AddEventFSM(StatesGroup):
    year = State()
    month = State()
    day = State()
    hour = State()
    minute = State()
    max_count_of_buyings = State()
    price = State()
    string_field = State()