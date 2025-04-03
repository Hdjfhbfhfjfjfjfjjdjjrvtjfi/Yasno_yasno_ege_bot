__all__ = ["router"]
from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tg_bot.filters.callback_data import QuestionSchoolGradeCallbackData
from tg_bot.filters.commands import add_question_command
from tg_bot.keyboards.get_question_school_grade_keyboard import get_get_question_school_grade_keyboard
from tg_bot.models import TestQuestion, SchoolGrade
from tg_bot.utils.constants import QUESTION_DATA_ARGUMENT_NAME
from tg_bot.utils.data_objects import QuestionData
from tg_bot.utils.texts import (get_get_question_description_text, get_get_count_of_question_answers_text,
                                get_get_answer_description_text, get_get_question_school_grade_text)
from tg_bot.states import AddQuestionFSM

router: Router = Router()


@router.message(Command(commands=[add_question_command]))
async def add_question_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.delete()
    question_data: QuestionData = QuestionData()
    question_data.last_message = await bot.send_message(
        chat_id=message.chat.id,
        text=get_get_question_school_grade_text(),
        reply_markup=get_get_question_school_grade_keyboard(await SchoolGrade.get_grades_tuple()),
    )
    await state.set_data({QUESTION_DATA_ARGUMENT_NAME: question_data})
    await state.set_state(AddQuestionFSM.school_grade)

@router.message(StateFilter(AddQuestionFSM.school_grade))
async def question_school_grade_incorrect_answer_handler(message: Message) -> None:
    await message.delete()

@router.callback_query(QuestionSchoolGradeCallbackData.filter(), StateFilter(AddQuestionFSM.school_grade))
async def question_school_grade_handler(call: CallbackQuery, state: FSMContext, question_data: QuestionData,
                                        callback_data: QuestionSchoolGradeCallbackData) -> None:
    question_data.school_grade = callback_data.grade
    await call.message.edit_text(
        text=get_get_question_description_text()
    )
    await state.set_state(AddQuestionFSM.question_description)



@router.message(StateFilter(AddQuestionFSM.question_description))
async def question_description_handler(message: Message, state: FSMContext, question_data: QuestionData) -> None:
    await message.delete()
    if message.text is not None:
        question_data.description = message.text
    elif message.caption is not None:
        question_data.description = message.caption
    if question_data.description is not None:
        await state.set_state(AddQuestionFSM.count_of_answers)
        await question_data.last_message.edit_text(
            text=get_get_count_of_question_answers_text()
        )

@router.message(StateFilter(AddQuestionFSM.count_of_answers))
async def get_count_of_question_answers_handler(message: Message, question_data: QuestionData, state: FSMContext
                                                ) -> None:
    await message.delete()
    text = None
    if message.text is not None:
        text = message.text
    elif message.caption is not None:
        text = message.caption
    if text is not None and text.isdigit():
        question_data.max_count_of_answers = int(text)
        await state.set_state(AddQuestionFSM.answer_description)
        await question_data.last_message.edit_text(
            text=get_get_answer_description_text(question_data.count_of_answers + 1)
        )

@router.message(StateFilter(AddQuestionFSM.answer_description))
async def get_answer_description_handler(message: Message, state: FSMContext, question_data: QuestionData):
    await message.delete()
    if message.text is not None:
        question_data.answers_descriptions.append(message.text)
    elif message.caption is not None:
        question_data.answers_descriptions.append(message.caption)
    if question_data.count_of_answers < question_data.max_count_of_answers:
        await question_data.last_message.edit_text(
            text=get_get_answer_description_text(question_data.count_of_answers + 1)
        )
    else:
        await TestQuestion.create_test_question(question_data)
        await question_data.last_message.delete()
        await state.clear()

