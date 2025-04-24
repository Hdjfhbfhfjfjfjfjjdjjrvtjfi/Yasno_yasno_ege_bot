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
    """Text content for the data processing agreement page.
    
    :return: The agreement text content
    """
    # TODO: write text
    return "agreement_on_data_processing_text"

def get_get_user_name_full_name_surname_page_text() -> str:
    """Text prompt for collecting user's full name.
    
    :return: The name input prompt text
    """
    return "Введите фамилию, имя и отчество разделенные пробелами"

def get_get_user_phone_number_page_text() -> str:
    """Text prompt for collecting user's phone number.
    
    :return: The phone number input prompt text
    """
    return "Введите номер телефона в формате +7..."
#</editor-fold>

#<editor-fold desc="Main menu texts">
def get_main_menu_page_text() -> str:
    """Text content for the main menu page.
    
    :return: The main menu text content
    """
    # TODO: Write text
    return "main_menu_text"
#</editor-fold>

# <editor-fold desc="Excursion buying texts">
def get_choose_excursion_date_page_text() -> str:
    """Text prompt for selecting an excursion date.
    
    :return: The date selection prompt text
    """
    # TODO: Write text
    return "choose_excursion_date_text"

def get_excursion_question_page_text() -> str:
    """Text content for the excursion question page.
    
    :return: The question text content
    """
    # TODO: Write text
    return "excursion_question_page_text"

def get_excursion_pay_page_text(excursion_time: datetime, excursion_address: str) -> str:
    """Text content for the excursion payment page.
    
    :param excursion_time: The scheduled time of the excursion
    :param excursion_address: The location address of the excursion
    :return: The payment page text with formatted time and address
    """
    # TODO: Write text
    return f"excursion_pay_page_text {excursion_time.strftime("%d %B %H:%M")} {excursion_address}"
# </editor-fold>

# <editor-fold desc="Knowledge assesment buying texts">
def get_choose_knowledge_assesment_date_page_text() -> str:
    """Text prompt for selecting a knowledge assessment date.
    
    :return: The date selection prompt text
    """
    # TODO: Write text
    return "choose_knowledge_assesment_date_text"

def get_knowledge_assesment_question_page_text() -> str:
    """Text content for the knowledge assessment question page.
    
    :return: The question text content
    """
    # TODO: Write text
    return "knowledge_assesment_question_page_text"

def get_knowledge_assesment_pay_page_text(date: datetime, webinar_link: str) -> str:
    """Text content for the knowledge assessment payment page.
    
    :param date: The scheduled date of the assessment
    :param webinar_link: The link to the webinar
    :return: The payment page text
    """
    # TODO: Write text
    return "knowledge_assesment_pay_page_text"
# </editor-fold>

# <editor-fold desc="Knowledge assesment test texts">
def get_get_user_grade_text() -> str:
    """Text prompt for collecting user's grade.
    
    :return: The grade input prompt text
    """
    # TODO: Write text
    return "get_user_grade_text"
# </editor-fold>

# <editor-fold desc="Support buying texts">
def get_payment_fail_text() -> str:
    """Text content for payment failure notification.
    
    :return: The payment failure message
    """
    return "Оплата не была проведена, либо платеж еще не обработан"

def get_payment_succed_go_back_text() -> str:
    """Text content for successful payment notification.
    
    :return: The success message with return prompt
    """
    # TODO: Write text
    return "payment_succed_go_back_text"
# </editor-fold>

# <editor-fold desc="User profile texts">
def get_user_profile_page_text(excursion: tuple[datetime, str] | None, knowledge_assesment: tuple[datetime, str] | None) -> str:
    """Text content for the user profile page.
    
    :param excursion: Tuple containing excursion time and address, or None if no excursion is scheduled
    :param knowledge_assesment: Tuple containing assessment time and link, or None if no assessment is scheduled
    :return: The profile page text with formatted excursion and assessment information
    """
    # TODO: Write text
    return (f"profile_page_text"
            f"{excursion[0].strftime("%d %B %H:%M") + excursion[1] if excursion is not None else str()}"
            f"{knowledge_assesment[0].strftime("%d %B %H:%M") + knowledge_assesment[1] if knowledge_assesment is not None else str()}")
# </editor-fold>

# <editor-fold desc="Add school grade">
def get_get_school_grade_grade_text() -> str:
    """Text prompt for adding a new school grade.
    
    :return: The grade input prompt text
    """
    return "Введите номер класса, который хотите добавить"
# </editor-fold>

# <editor-fold desc="Add question">
def get_get_question_school_grade_text() -> str:
    """Text prompt for selecting a question's target grade.
    
    :return: The school grade selection prompt text
    """
    return "Выберите класс, к которому относится вопрос"

def get_get_question_description_text() -> str:
    """Text prompt for entering a question description.
    
    :return: The question description input prompt text
    """
    return "Введите формулировку вопроса"

def get_get_count_of_question_answers_text() -> str:
    """Text prompt for specifying the number of answers.
    
    :return: The answer count input prompt text
    """
    return "Введите количество ответов на вопрос"

def get_get_answer_description_text(answer_number: int) -> str:
    """Text prompt for entering an answer description.
    
    :param answer_number: The sequential number of the answer being entered
    :return: The answer description input prompt text
    """
    return f"Введите ответ №{answer_number}"
# </editor-fold>

# <editor-fold desc="Add event">
def get_get_event_year_text() -> str:
    """Text prompt for entering an event's year.
    
    :return: The year input prompt text
    """
    return "Введите год, в который пройдет событие"

def get_get_event_month_text() -> str:
    """Text prompt for entering an event's month.
    
    :return: The month input prompt text
    """
    return "Введите месяц, в который пройдет событие"

def get_get_event_day_text() -> str:
    """Text prompt for entering an event's day.
    
    :return: The day input prompt text
    """
    return "Введите день, в который пройдет событие"

def get_get_event_hour_text() -> str:
    """Text prompt for entering an event's hour.
    
    :return: The hour input prompt text
    """
    return "Введите час, в который пройдет событие"

def get_get_event_minute_text() -> str:
    """Text prompt for entering an event's minute.
    
    :return: The minute input prompt text
    """
    return "Введите минуту, в котоую пройдет событие"

def get_get_event_max_count_of_buyings_text() -> str:
    """Text prompt for entering an event's maximum capacity.
    
    :return: The maximum capacity input prompt text
    """
    return "Введите максимальное число посетителей события"

def get_get_event_price_text() -> str:
    """Text prompt for entering an event's price.
    
    :return: The price input prompt text
    """
    return "Введите цену посещения события"

def get_get_excursion_address_text() -> str:
    """Text prompt for entering an excursion's address.
    
    :return: The address input prompt text
    """
    return "Введите адрес, в котором начнется экскурсия"

def get_get_knowledge_assesment_link_text() -> str:
    """Text prompt for entering a knowledge assessment's webinar link.
    
    :return: The webinar link input prompt text
    """
    return "Введите ссылку на вебинар по оценке знаний"
# </editor-fold>


