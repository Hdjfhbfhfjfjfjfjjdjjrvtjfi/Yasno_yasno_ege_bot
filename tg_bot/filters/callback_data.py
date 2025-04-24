from __future__ import annotations
__all__ = ["GetUserDataPageCallbackData", "ChooseEventDatePageCallbackData", "UserProfilePageCallbackData",
           "EventPageCallbackData", "EventQuestionPageCallbackData", "MainMenuPageCallbackData",
           "ChooseEventDatePageSwitchKeyboardCallbackData", "EventCheckPaymentPageCallbackData",
           "GetUserGradeCallbackData", "GetResponseToQuestionCallbackData", "QuestionSchoolGradeCallbackData"]
from aiogram.filters.callback_data import CallbackData

from tg_bot.utils.enums import EventEnum


# <editor-fold desc="Registration and main menu callback data">
class GetUserDataPageCallbackData(CallbackData, prefix="get_user"):
    """Callback data for navigating to the user data collection page.
    
    This class represents the callback data used when a user agrees to the data processing agreement
    and proceeds to provide their personal information.
    """
    pass

class MainMenuPageCallbackData(CallbackData, prefix="mainmenu"):
    """Callback data for navigating to the main menu page.
    
    This class represents the callback data used when a user wants to return to the main menu
    from any other page in the application.
    """
    pass
# </editor-fold>

# <editor-fold desc="User profile callback data">
class UserProfilePageCallbackData(CallbackData, prefix="user_profile"):
    """Callback data for navigating to the user profile page.
    
    This class represents the callback data used when a user wants to view their profile information.
    """
    pass
# </editor-fold>

# <editor-fold desc="Event payment callback data">
class ChooseEventDatePageCallbackData(CallbackData, prefix="choose_excursion_date"):
    """Callback data for navigating to the event date selection page.
    
    This class represents the callback data used when selecting an event date.
    
    :ivar event: Type of the event (excursion or knowledge assessment)
    :ivar page_index: Index of the current page in pagination (default: 0)
    """
    event: EventEnum
    page_index: int = 0

class ChooseEventDatePageSwitchKeyboardCallbackData(CallbackData, prefix="choose_excursion_date_switch_keyboard"):
    """Callback data for switching between pages in the event date selection.
    
    This class represents the callback data used when navigating between different pages
    of available event dates.
    
    :ivar event: Type of the event (excursion or knowledge assessment)
    :ivar page_index: Index of the target page in pagination
    """
    event: EventEnum
    page_index: int

class EventPageCallbackData(CallbackData, prefix="excursion_page"):
    """Callback data for navigating to a specific event page.
    
    This class represents the callback data used when selecting a specific event
    from the list of available events.
    
    :ivar event: Type of the event (excursion or knowledge assessment)
    :ivar id: UUID of the selected event
    :ivar page_index: Index of the current page in pagination
    """
    event: EventEnum
    id: str
    page_index: int

class EventQuestionPageCallbackData(CallbackData, prefix="excursion_question_page"):
    """Callback data for navigating to the event question page.
    
    This class represents the callback data used when a user wants to ask a question
    about a specific event.
    
    :ivar event: Type of the event (excursion or knowledge assessment)
    :ivar page_index: Index of the current page in pagination
    """
    event: EventEnum
    page_index: int

class EventCheckPaymentPageCallbackData(CallbackData, prefix="excursion_check_payment_page"):
    """Callback data for navigating to the event payment check page.
    
    This class represents the callback data used when a user wants to check the status
    of their event payment.
    
    :ivar event: Type of the event (excursion or knowledge assessment)
    """
    event: EventEnum
# </editor-fold>

# <editor-fold desc="Knowledge assesment test callback data">
class GetUserGradeCallbackData(CallbackData, prefix="get_user_grade"):
    """Callback data for selecting a user's grade
    
    This class represents the callback data used when a user selects their grade
    during the knowledge assessment process.
    
    :ivar grade: Selected grade
    """
    grade: int

class GetResponseToQuestionCallbackData(CallbackData, prefix="get_response_to_question"):
    """Callback data for submitting an answer to a knowledge assessment question.
    
    This class represents the callback data used when a user selects an answer
    during the knowledge assessment test.
    
    :ivar answer_id: ID of the selected answer
    """
    answer_id: str
# </editor-fold>

# <editor-fold desc="Add question callback data">
class QuestionSchoolGradeCallbackData(CallbackData, prefix="question_school_grade"):
    """Callback data for selecting a school grade when adding a question.
    
    This class represents the callback data used when selecting a school grade
    for a new question.
    
    :ivar grade: Selected school grade
    """
    grade: int
# </editor-fold>
