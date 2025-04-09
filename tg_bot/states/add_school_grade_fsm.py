__all__ = ["AddSchoolGradeFSM"]
from aiogram.fsm.state import State, StatesGroup

class AddSchoolGradeFSM(StatesGroup):
    grade = State()