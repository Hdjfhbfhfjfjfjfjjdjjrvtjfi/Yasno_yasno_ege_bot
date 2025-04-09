__all__ = ["router"]
from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from tg_bot.filters.commands import add_school_grade_command
from tg_bot.models import SchoolGrade
from tg_bot.utils.data_objects import SchoolGradeData
from tg_bot.states import AddSchoolGradeFSM
from tg_bot.utils.texts import get_get_school_grade_grade_text
from tg_bot.utils.constants import SCHOOL_GRADE_DATA_ARGUMENT_NAME


router: Router = Router()


@router.message(Command(commands=[add_school_grade_command]))
async def add_school_grade_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    school_grade_data: SchoolGradeData = SchoolGradeData()
    school_grade_data.message = await bot.send_message(
        chat_id=message.chat.id,
        text=get_get_school_grade_grade_text()
    )
    await state.set_state(AddSchoolGradeFSM.grade)
    await state.set_data({SCHOOL_GRADE_DATA_ARGUMENT_NAME: school_grade_data})

@router.message(StateFilter(AddSchoolGradeFSM.grade))
async def get_school_grade_grade_handler(message: Message, state: FSMContext, school_grade_data: SchoolGradeData):
    await message.delete()
    if message.text is not None and message.text.isdigit():
        school_grade_data.grade = int(message.text)
    elif message.caption is not None and message.caption.isdigit():
        school_grade_data.grade = int(message.caption)
    if school_grade_data.grade is not None:
        await SchoolGrade.create_school_grade(school_grade_data)
        await school_grade_data.message.delete()
        await state.clear()



