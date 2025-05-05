__all__= ["KnowledgeAssesmentTestHandler"]
from aiogram.handlers import CallbackQueryHandler

from typing import Any

from abc import abstractmethod

from tg_bot.utils.data_objects import TestResultData
from tg_bot.models import TestQuestion, User, TestResult
from tg_bot.utils.wrap_classes import KnowledgeAssesmentProfile
from tg_bot.utils.texts import get_main_menu_page_text
from tg_bot.utils.mixins import ConfigMixin, DataObjectMixin
from tg_bot.keyboards import get_main_menu_page_keyboard, get_knowledge_assesment_question_keyboard


class KnowledgeAssesmentTestHandler(CallbackQueryHandler, ConfigMixin, DataObjectMixin[TestResultData]):
    """Base class for handling test-related functionality."""

    @abstractmethod
    def handle(self) -> Any:
        raise NotImplementedError

    async def display_question(self, question: TestQuestion) -> None:
        """Display a question and its answers to the user."""
        answers = tuple(
            map(lambda t: (str(t[0]), t[1]),
                await question.answers.all().values_list("id", "description"))
        )
        await self.message.edit_text(text=question.description)
        await self.message.edit_reply_markup(
            reply_markup=get_knowledge_assesment_question_keyboard(answers)
        )

    async def handle_test_completion(self) -> None:
        """Handle the completion of a test."""
        user_profile = await (await User.get_user_by_id(self.message.chat.id)).get_user_profile()
        test_result = await TestResult.create_test_result(self.data_object)

        await user_profile.set_knowledge_assesment_profile(
            KnowledgeAssesmentProfile(
                self.data_object.knowledge_assesment,
                test_result
            )
        )

        await self.message.edit_text(text=get_main_menu_page_text())
        await self.message.edit_reply_markup(
            reply_markup=get_main_menu_page_keyboard(
                self.config.connection_link,
                await user_profile.has_excursion(),
                await user_profile.has_knowledge_assesment()
            )
        )