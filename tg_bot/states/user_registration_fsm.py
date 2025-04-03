__all__ = ["UserRegistrationFSM"]
from aiogram.fsm.state import State, StatesGroup


class UserRegistrationFSM(StatesGroup):
    name_full_name_surname = State()
    phone_number = State()
