__all__ = ["AddSchoolGradeFSM"]
from aiogram.fsm.state import State, StatesGroup

class AddSchoolGradeFSM(StatesGroup):
    """Finite State Machine for managing the school grade creation process.
    
    :ivar grade: State for collecting the school grade number
    """
    grade = State()