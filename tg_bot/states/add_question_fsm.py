__all__ = ["AddQuestionFSM"]
from aiogram.fsm.state import State, StatesGroup


class AddQuestionFSM(StatesGroup):
    school_grade = State()
    question_description = State()
    count_of_answers = State()
    answer_description = State()