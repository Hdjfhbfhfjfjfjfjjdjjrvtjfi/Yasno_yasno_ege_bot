__all__ = ["router"]
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import TelegramObject

from tg_bot.handlers.abstract_handlers import FormBaseHandler
from tg_bot.filters.callback_data import QuestionSchoolGradeCallbackData
from tg_bot.filters.commands import add_question_command
from tg_bot.keyboards.get_question_school_grade_keyboard import get_get_question_school_grade_keyboard
from tg_bot.models import SchoolGrade
from tg_bot.utils.constants import QUESTION_DATA_ARGUMENT_NAME
from tg_bot.utils.data_objects import QuestionData
from tg_bot.utils.enums import HandlerTypeEnum
from tg_bot.utils.message_builders import TextMessageBuilder
from tg_bot.utils.mixins import CommandMixin, UnpackedCallbackDataMixin
from tg_bot.utils.texts import (get_get_question_description_text, get_get_count_of_question_answers_text,
                                get_get_answer_description_text, get_get_question_school_grade_text)
from tg_bot.states import AddQuestionFSM


router: Router = Router()

@router.message(Command(commands=[add_question_command]))
class AddQuestionHandler(FormBaseHandler[QuestionData], CommandMixin, handler_type=HandlerTypeEnum.first_handler):
    async def handle(self) -> None:
        grades: tuple[int, ...] = await SchoolGrade.get_grades_tuple()
        await self.initialize_form_data(
            QuestionData(),
            TextMessageBuilder.send_new_message(get_get_question_school_grade_text(), self.bot, self.event.chat.id).
            edit_reply_markup(get_get_question_school_grade_keyboard(grades)),
            AddQuestionFSM.school_grade,
            QUESTION_DATA_ARGUMENT_NAME
        )

@router.callback_query(QuestionSchoolGradeCallbackData.filter(), StateFilter(AddQuestionFSM.school_grade))
class GetQuestionSchoolGradeHandler(UnpackedCallbackDataMixin[QuestionSchoolGradeCallbackData],
                                    FormBaseHandler[QuestionData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = QUESTION_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self) -> None:
        self.data_object.school_grade = await self.process_numeric_state(
            AddQuestionFSM.question_description,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_question_description_text())
        )

    async def _process_callback_data(self) -> str | None:
        return str(self.unpacked_callback_data.grade)



@router.message(StateFilter(AddQuestionFSM.question_description))
class GetQuestionDescriptionHandler(FormBaseHandler[QuestionData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = QUESTION_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self) -> None:
        self.data_object.description = await self.process_text_state(
            AddQuestionFSM.count_of_answers,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_count_of_question_answers_text())
        )

@router.message(StateFilter(AddQuestionFSM.count_of_answers))
class GetCountOfQuestionAnswersHandler(FormBaseHandler[QuestionData]):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = QUESTION_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self) -> None:
        self.data_object.max_count_of_answers = await self.process_numeric_state(
            AddQuestionFSM.answer_description,
            TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
            edit_text(get_get_answer_description_text(1))
        )

@router.message(StateFilter(AddQuestionFSM.answer_description))
class GetAnswerDescriptionHandler(FormBaseHandler[QuestionData], handler_type=HandlerTypeEnum.get_info_handler):

    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = QUESTION_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self) -> None:
        if self.data_object.count_of_answers < self.data_object.max_count_of_answers - 1:
            type(self).handler_type = HandlerTypeEnum.get_info_handler
        else:
            type(self).handler_type = HandlerTypeEnum.final_handler
        self.data_object.answers_descriptions.append(
            await self.process_text_state(
                AddQuestionFSM.answer_description,
                TextMessageBuilder.create_from_existing_message(self.data_object.last_message).
                edit_text(get_get_answer_description_text(self.data_object.count_of_answers + 2))
            )
        )
        if len(self.data_object.answers_descriptions) == self.data_object.max_count_of_answers:
            await self.data_object.create_model_instance()

