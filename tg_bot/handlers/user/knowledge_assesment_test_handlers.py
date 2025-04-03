__all__ = ["router"]
from aiogram import Router
from aiogram.types import CallbackQuery

from tg_bot.models import SchoolGrade, TestQuestion, TestResponse, TestAnswer, TestResult, User
from tg_bot.keyboards import get_knowledge_assesment_question_keyboard, get_main_menu_page_keyboard
from tg_bot.filters.callback_data import GetUserGradeCallbackData, GetResponseToQuestionCallbackData
from tg_bot.utils.config import Config
from tg_bot.utils.data_objects import TestResultData
from tg_bot.utils.wrap_classes import KnowledgeAssesmentProfile
from tg_bot.utils.texts import get_main_menu_page_text


router: Router = Router()


@router.callback_query(GetUserGradeCallbackData.filter())
async def get_user_grade_handler(call: CallbackQuery, test_result_data: TestResultData,
                                 callback_data: GetUserGradeCallbackData) -> None:
    test_result_data.grade = await SchoolGrade.get_by_id(callback_data.grade)
    test_result_data.questions = await test_result_data.grade.questions.filter()
    question: TestQuestion = test_result_data.questions[test_result_data.question_number]
    answers: tuple[tuple[str, str], ...] = tuple(map(lambda t: (str(t[0]), t[1]), await question.answers.all().values_list("id", "description")))
    await call.message.edit_text(
        text=question.description
    )
    await call.message.edit_reply_markup(
        reply_markup=get_knowledge_assesment_question_keyboard(answers)
    )

@router.callback_query(GetResponseToQuestionCallbackData.filter())
async def get_response_to_question_handler(call: CallbackQuery, test_result_data: TestResultData, config: Config,
                                           callback_data: GetResponseToQuestionCallbackData) -> None:
    test_response = await TestResponse.create_test_response(
        test_result_data.questions[test_result_data.question_number],
        await TestAnswer.get_by_id(callback_data.answer_id)
    )
    test_result_data.responses.append(test_response)
    test_result_data.question_number += 1
    if test_result_data.question_number == len(test_result_data.questions):
        user_profile = await (await User.get_user_by_id(call.message.chat.id)).get_user_profile()
        await user_profile.set_knowledge_assesment_profile(
            KnowledgeAssesmentProfile(
                test_result_data.knowledge_assesment,
                await TestResult.create_test_result(test_result_data)
            )
        )
        await call.message.edit_text(
            text=get_main_menu_page_text()
        )
        await call.message.edit_reply_markup(
            reply_markup=get_main_menu_page_keyboard(
                config.connection_link,
                await user_profile.has_excursion(),
                await user_profile.has_knowledge_assesment()
            )
        )
    else:
        question: TestQuestion = test_result_data.questions[test_result_data.question_number]
        answers: tuple[tuple[str, str], ...] = tuple(map(lambda t: (str(t[0]), t[1]), await question.answers.all().values_list("id", "description")))
        await call.message.edit_text(
            text=question.description
        )
        await call.message.edit_reply_markup(
            reply_markup=get_knowledge_assesment_question_keyboard(answers)
        )
