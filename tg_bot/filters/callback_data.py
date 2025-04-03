__all__ = ["GetUserDataPageCallbackData", "ChooseEventDatePageCallbackData", "UserProfilePageCallbackData",
           "EventPageCallbackData", "EventQuestionPageCallbackData", "MainMenuPageCallbackData",
           "ChooseEventDatePageSwitchKeyboardCallbackData", "EventCheckPaymentPageCallbackData",
           "GetUserGradeCallbackData", "GetResponseToQuestionCallbackData", "QuestionSchoolGradeCallbackData"]
from aiogram.filters.callback_data import CallbackData

from tg_bot.utils.enums import EventEnum


# <editor-fold desc="Registration and main menu callback data">
class GetUserDataPageCallbackData(CallbackData, prefix="get_user"):
    pass

class MainMenuPageCallbackData(CallbackData, prefix="mainmenu"):
    pass
# </editor-fold>

# <editor-fold desc="User profile callback data">
class UserProfilePageCallbackData(CallbackData, prefix="user_profile"):
    pass
# </editor-fold>

# <editor-fold desc="Event payment callback data">
class ChooseEventDatePageCallbackData(CallbackData, prefix="choose_excursion_date"):
    event: EventEnum
    page_index: int = 0

class ChooseEventDatePageSwitchKeyboardCallbackData(CallbackData, prefix="choose_excursion_date_switch_keyboard"):
    event: EventEnum
    page_index: int

class EventPageCallbackData(CallbackData, prefix="excursion_page"):
    event: EventEnum
    id: str
    page_index: int

class EventQuestionPageCallbackData(CallbackData, prefix="excursion_question_page"):
    event: EventEnum
    page_index: int

class EventCheckPaymentPageCallbackData(CallbackData, prefix="excursion_check_payment_page"):
    event: EventEnum
# </editor-fold>

# <editor-fold desc="Knowledge assesment test callback data">
class GetUserGradeCallbackData(CallbackData, prefix="get_user_grade"):
    grade: int

class GetResponseToQuestionCallbackData(CallbackData, prefix="get_response_to_question"):
    answer_id: str
# </editor-fold>

# <editor-fold desc="Add question callback data">
class QuestionSchoolGradeCallbackData(CallbackData, prefix="question_school_grade"):
    grade: int
# </editor-fold>
