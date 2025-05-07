__all__ = ["router"]
from abc import abstractmethod
from typing import Any

from aiogram import Router
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import CallbackQuery, TelegramObject

from tg_bot.models import SchoolGrade, TestResponse, TestAnswer
from tg_bot.filters.callback_data import GetUserGradeCallbackData, GetResponseToQuestionCallbackData
from tg_bot.utils.mixins import UnpackedCallbackDataMixin
from tg_bot.utils.constants import TEST_RESULT_DATA_ARGUMENT_NAME
from tg_bot.handlers.abstract_handlers import KnowledgeAssesmentTestHandler


router: Router = Router()


@router.callback_query(GetUserGradeCallbackData.filter())
class GetUserGradeHandlerKnowledgeAssesment(UnpackedCallbackDataMixin[GetUserGradeCallbackData],
                                            KnowledgeAssesmentTestHandler):
    """Do not change the order of class inheritance"""
    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = TEST_RESULT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        self.data_object.grade = await SchoolGrade.get_by_id(self.unpacked_callback_data.grade)
        self.data_object.questions = await self.data_object.grade.questions.filter()
        question = self.data_object.questions[self.data_object.question_number]
        await self.display_question(question)


@router.callback_query(GetResponseToQuestionCallbackData.filter())
class GetResponseToQuestionHandlerKnowledgeAssesment(UnpackedCallbackDataMixin[GetResponseToQuestionCallbackData],
                                                     KnowledgeAssesmentTestHandler):
    """Do not change the order of class inheritance"""
    def __init__(self, event: TelegramObject, **kwargs) -> None:
        self._data_object_argument_name = TEST_RESULT_DATA_ARGUMENT_NAME
        super().__init__(event, **kwargs)

    async def handle(self):
        test_response = await TestResponse.create_test_response(
            self.data_object.questions[self.data_object.question_number],
            await TestAnswer.get_by_id(self.unpacked_callback_data.answer_id)
        )
        self.data_object.responses.append(test_response)
        self.data_object.question_number += 1
        if self.data_object.question_number == len(self.data_object.questions):
            await self.handle_test_completion()
        else:
            question = self.data_object.questions[self.data_object.question_number]
            await self.display_question(question)
