__all__ = ["UserRegistrationFSM"]
from aiogram.fsm.state import State, StatesGroup


class UserRegistrationFSM(StatesGroup):
    """Finite State Machine for managing the user registration process.
    
    :ivar name_full_name_surname: State for collecting the user's full name
    :ivar phone_number: State for collecting the user's phone number
    """
    name_full_name_surname = State()
    phone_number = State()
