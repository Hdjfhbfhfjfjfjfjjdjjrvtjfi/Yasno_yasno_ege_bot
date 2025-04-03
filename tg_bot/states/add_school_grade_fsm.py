__all__ = ["AddSchoolGradeFsm"]
from aiogram.fsm.state import State, StatesGroup

class AddSchoolGradeFsm(StatesGroup):
    grade = State()