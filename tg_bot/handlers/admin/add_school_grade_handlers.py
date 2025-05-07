__all__ = ["router"]
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import TelegramObject

from tg_bot.handlers.abstract_handlers import FormBaseHandler
from tg_bot.filters.commands import add_school_grade_command
from tg_bot.utils.data_objects import SchoolGradeData
from tg_bot.states import AddSchoolGradeFSM
from tg_bot.utils.enums import HandlerTypeEnum
from tg_bot.utils.message_builders import TextMessageBuilder
from tg_bot.utils.texts import get_get_school_grade_grade_text
from tg_bot.utils.constants import SCHOOL_GRADE_DATA_ARGUMENT_NAME


router: Router = Router()


@router.message(Command(commands=[add_school_grade_command]))
class AddSchoolGradeHandler(FormBaseHandler[SchoolGradeData], handler_type=HandlerTypeEnum.first_handler):
    async def handle(self) -> None:
        await self.initialize_form_data(
            SchoolGradeData(),
            TextMessageBuilder.send_new_message(get_get_school_grade_grade_text(), self.bot, self.event.chat.id),
            AddSchoolGradeFSM.grade,
            SCHOOL_GRADE_DATA_ARGUMENT_NAME
        )

@router.message(StateFilter(AddSchoolGradeFSM.grade))
class GetSchoolGradeGradeHandler(FormBaseHandler[SchoolGradeData], handler_type=HandlerTypeEnum.final_handler):

    def __init__(self, event: TelegramObject, **kwargs):
        self._data_object_argument_name = SCHOOL_GRADE_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.grade = await self.process_numeric_state(
            AddSchoolGradeFSM.grade,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message)
        )
        if self.data_object.grade is not None:
            await self.data_object.create_model_instance()