__all__ = ["agreement_on_data_processing_page_text", "get_main_menu_page_text", "get_get_user_phone_number_page_text",
           "get_get_user_name_full_name_surname_page_text", "get_choose_excursion_date_page_text",
           "get_excursion_question_page_text", "get_excursion_pay_page_text", "get_user_profile_page_text",
           "get_knowledge_assesment_pay_page_text", "get_knowledge_assesment_question_page_text",
           "get_choose_knowledge_assesment_date_page_text", "get_payment_fail_text", "get_get_user_grade_text",
           "get_get_school_grade_grade_text", "get_get_question_description_text", "get_get_question_school_grade_text",
           "get_get_count_of_question_answers_text", "get_get_answer_description_text",
           "get_get_knowledge_assesment_link_text", "get_get_excursion_address_text", "get_get_event_hour_text",
           "get_get_event_year_text", "get_get_event_day_text", "get_get_event_minute_text", "get_get_event_month_text",
           "get_get_event_price_text", "get_get_event_max_count_of_buyings_text", "get_payment_succed_go_back_text"]
from datetime import datetime


#<editor-fold desc="Registration of user texts">
def agreement_on_data_processing_page_text() -> str:
    return "agreement_on_data_processing_text"

def get_get_user_name_full_name_surname_page_text() -> str:
    return "get_user_name_full_name_surname_text"

def get_get_user_phone_number_page_text() -> str:
    return "get_user_phone_number_text"
#</editor-fold>

#<editor-fold desc="Main menu texts">
def get_main_menu_page_text() -> str:
    return "main_menu_text"
#</editor-fold>

# <editor-fold desc="Excursion buying texts">
def get_choose_excursion_date_page_text() -> str:
    return "choose_excursion_date_text"

def get_excursion_question_page_text() -> str:
    return "excursion_question_page_text"

def get_excursion_pay_page_text(excursion_time: datetime, excursion_address: str) -> str:
    return f"excursion_pay_page_text {excursion_time.strftime("%d %B %H:%M")} {excursion_address}"
# </editor-fold>

# <editor-fold desc="Knowledge assesment buying texts">
def get_choose_knowledge_assesment_date_page_text() -> str:
    return "choose_knowledge_assesment_date_text"

def get_knowledge_assesment_question_page_text() -> str:
    return "knowledge_assesment_question_page_text"

def get_knowledge_assesment_pay_page_text(date: datetime, webinar_link: str) -> str:
    return "knowledge_assesment_pay_page_text"
# </editor-fold>

# <editor-fold desc="Knowledge assesment test texts">
def get_get_user_grade_text() -> str:
    return "get_user_grade_text"
# </editor-fold>

# <editor-fold desc="Support buying texts">
def get_payment_fail_text() -> str:
    return "payment_fail_text"

def get_payment_succed_go_back_text() -> str:
    return "payment_succed_go_back_text"
# </editor-fold>

# <editor-fold desc="User profile texts">
def get_user_profile_page_text(excursion: tuple[datetime, str] | None, knowledge_assesment: tuple[datetime, str] | None) -> str:
    return (f"profile_page_text"
            f"{excursion[0].strftime("%d %B %H:%M") + excursion[1] if excursion is not None else str()}"
            f"{knowledge_assesment[0].strftime("%d %B %H:%M") + knowledge_assesment[1] if knowledge_assesment is not None else str()}")
# </editor-fold>

# <editor-fold desc="Add school grade">
def get_get_school_grade_grade_text() -> str:
    return "get_school_grade_grade_text"
# </editor-fold>

# <editor-fold desc="Add question">
def get_get_question_school_grade_text() -> str:
    return "get_question_school_grade_text"

def get_get_question_description_text() -> str:
    return "get_question_description_text"

def get_get_count_of_question_answers_text() -> str:
    return "get_count_of_qustion_answers_text"

def get_get_answer_description_text(answer_number: int) -> str:
    return f"get_answer_number_{answer_number}_description_text"
# </editor-fold>

# <editor-fold desc="Add event">
def get_get_event_year_text() -> str:
    return "get_event_year_text"

def get_get_event_month_text() -> str:
    return "get_event_month_text"

def get_get_event_day_text() -> str:
    return "get_event_day_text"

def get_get_event_hour_text() -> str:
    return "get_event_hour_text"

def get_get_event_minute_text() -> str:
    return "get_event_minute_text"

def get_get_event_max_count_of_buyings_text() -> str:
    return "get_event_max_count_of_buyings_text"

def get_get_event_price_text() -> str:
    return "get_event_price_text"

def get_get_excursion_address_text() -> str:
    return "get_excursion_address_text"

def get_get_knowledge_assesment_link_text() -> str:
    return "get_knowledge_assesment_link_text"
# </editor-fold>


