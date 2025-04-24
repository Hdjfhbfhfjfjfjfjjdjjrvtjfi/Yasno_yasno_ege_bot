__all__ = ["AddQuestionFSM"]
from aiogram.fsm.state import State, StatesGroup


class AddQuestionFSM(StatesGroup):
    """Finite State Machine for managing the question creation process.
    
    :ivar school_grade: State for collecting the target school grade
    :ivar question_description: State for collecting the question text
    :ivar count_of_answers: State for collecting the number of possible answers
    :ivar answer_description: State for collecting the answer text
    """
    school_grade = State()
    question_description = State()
    count_of_answers = State()
    answer_description = State()
