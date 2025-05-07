__all__ = ["agreement_on_data_processing_page_text", "get_main_menu_page_text", "get_get_user_phone_number_page_text",
           "get_get_user_name_full_name_surname_page_text", "get_choose_excursion_date_page_text",
           "get_excursion_question_page_text", "get_excursion_pay_page_text", "get_user_profile_page_text",
           "get_knowledge_assesment_pay_page_text", "get_knowledge_assesment_question_page_text",
           "get_choose_knowledge_assesment_date_page_text", "get_payment_fail_text", "get_get_user_grade_text",
           "get_get_school_grade_grade_text", "get_get_question_description_text", "get_get_question_school_grade_text",
           "get_get_count_of_question_answers_text", "get_get_answer_description_text",
           "get_get_knowledge_assesment_link_text", "get_get_excursion_address_text", "get_get_event_hour_text",
           "get_get_event_year_text", "get_get_event_day_text", "get_get_event_minute_text", "get_get_event_month_text",
           "get_get_event_price_text", "get_get_event_max_count_of_buyings_text", "get_payment_succed_go_back_text",
           "get_excursion_after_buy_text", "get_knowledge_assesment_after_buy_page_text",
           "get_knowledge_assesment_after_buy_first_guide_page_text",
           "get_knowledge_assesment_after_buy_second_guide_page_text"]
from datetime import datetime


#<editor-fold desc="Registration of user texts">
def agreement_on_data_processing_page_text() -> str:
    """Text content for the data processing agreement page.
    
    :return: The agreement text content
    """
    return ("Здравствуйте!\n"
            "Меня зовут Кибардина Мария Петровна. Я репетитор по русскому языку. "
            "В этом боте вы можете записаться на урок или квест и получить ответ на вопрос."
            "Для этого нажмите на кнопку \"Согласен\".\n"
            "✅ При регистрации я даю согласие на обработку моих персональных данных "
            "в соответствии ФЗ от 27.07.2006 года №152-ФЗ \"О персональных данных\".")

def get_get_user_name_full_name_surname_page_text() -> str:
    """Text prompt for collecting user's full name.
    
    :return: The name input prompt text
    """
    return "Введите фамилию, имя и отчество разделенные пробелами."

def get_get_user_phone_number_page_text() -> str:
    """Text prompt for collecting user's phone number.
    
    :return: The phone number input prompt text
    """
    return "Введите номер телефона в формате +71234567890."
#</editor-fold>

#<editor-fold desc="Main menu texts">
def get_main_menu_page_text() -> str:
    """Text content for the main menu page.
    
    :return: The main menu text content
    """
    return ("▶️Если Вы хотите увлекательно провести досуг "
            "и при этом узнать интересные факты о русском языке, запишитесь на квест \"Тайны русского языка\".\n"
            "▶️Если Вас волнуют оценки по русскому языку и вы хотите узнать, "
            "какие темы подтянуть, пройдите тест, соответствующий вашему возрасту.\n"
            "▶️Если у Вас другая задача, нажмите \"Получить ответ на вопрос\".")
#</editor-fold>

# <editor-fold desc="Excursion buying texts">
def get_choose_excursion_date_page_text() -> str:
    """Text prompt for selecting an excursion date.
    
    :return: The date selection prompt text
    """
    return ("Дорогой друг, квест по русскому языку \"Тайны русского языка\" создан для семей с детьми, "
            "которые желают прикоснуться к истории русского языка, услышать втский говор, увидеть берестяную грамоту,"
            "разгадать все секреты и почувствовать себя победителями.\n"
            "Выберите дату и время квеста.")

def get_excursion_question_page_text() -> str:
    """Text content for the excursion question page.
    
    :return: The question text content
    """
    return ("К сожалению, это время занято. "
            "Вернитесь на шаг назад и выберите другое время.\n"
            "Возможно у вас другая проблема. Тогда задайте вопрос.")

def get_excursion_pay_page_text(excursion_time: datetime, excursion_address: str) -> str:
    """Text content for the excursion payment page.
    
    :param excursion_time: The scheduled time of the excursion
    :param excursion_address: The location address of the excursion
    :return: The payment page text with formatted time and address
    """
    return (f"Бронирование записи на квест \"Тайны русского языка\" "
            f"на дату {excursion_time.strftime("%d.%m.%y и время %H:%M")}, по адресу {excursion_address}.")

def get_excursion_after_buy_text(excursion_address: str) -> str:
    return (f"Ждем по адресу {excursion_address}\n"
            f"Время проведенное с семей в интересной деятельности бесценно.")
# </editor-fold>

# <editor-fold desc="Knowledge assesment buying texts">
def get_choose_knowledge_assesment_date_page_text() -> str:
    """Text prompt for selecting a knowledge assessment date.
    
    :return: The date selection prompt text
    """
    return ("Мы обсудим в чем именно требуется моя помощь, вместе сформулируем запрос, "
            "затем начнем работать над задачей.\n"
            "Выберите дату и время занятия.")

def get_knowledge_assesment_question_page_text() -> str:
    """Text content for the knowledge assessment question page.
    
    :return: The question text content
    """
    return ("К сожалению, это время занято."
            "Вернитесь на шаг назад и выберите другое время.\n"
            "Возможно у вас другая проблема. Тогда задайте вопрос.")

def get_knowledge_assesment_pay_page_text(knowledge_assesment_date: datetime) -> str:
    """Text content for the knowledge assessment payment page.
    
    :param knowledge_assesment_date: The scheduled date of the assessment
    :return: The payment page text
    """
    return (f"Бронирование записи на занятие "
            f"на дату {knowledge_assesment_date.strftime("%d.%m.%y и время %H:%M")}")

def get_knowledge_assesment_after_buy_first_guide_page_text(knowledge_assesment_link: str) -> str:
    return (f"Дорогой друг, вы записались на занятие. Благодарю вас! "
            f"В назначенное время прошу вас пройти по ссылке {knowledge_assesment_link}.\n"
            f"Это вебинарная комната российской платформы pruffme.")

def get_knowledge_assesment_after_buy_second_guide_page_text() -> str:
    return "Чтобы я вас увидела и услышала, нажмите на значок камеры и микрофона."

def get_knowledge_assesment_after_buy_page_text() -> str:
    return "До встречи!"
# </editor-fold>

# <editor-fold desc="Knowledge assesment test texts">
def get_get_user_grade_text() -> str:
    """Text prompt for collecting user's grade.
    
    :return: The grade input prompt text
    """
    return "Выберите класс, в котором вы учитесь."
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
    return "Платеж успешно обработан, нажмите на кнопку \"Проверить оплату\""
# </editor-fold>

# <editor-fold desc="User profile texts">
def get_user_profile_page_text(excursion: tuple[datetime, str] | None, knowledge_assesment: tuple[datetime, str] | None) -> str:
    """Text content for the user profile page.
    
    :param excursion: Tuple containing excursion time and address, or None if no excursion is scheduled
    :param knowledge_assesment: Tuple containing assessment time and link, or None if no assessment is scheduled
    :return: The profile page text with formatted excursion and assessment information
    """
    return (f"{"Вы не записаны никуда." if excursion is None and knowledge_assesment is None else ""}"
            f"{f"Вы записаны на экскурсию по адресу {excursion[1]} на дату "
               f"{excursion[0].strftime("%d.%m.%y и время %H:%M")}.\n" if excursion is not None else ""}"
            f"{f"Вы записаны на занятие на дату {knowledge_assesment[0].strftime("%d.%m.%y и время %H:%M")}, "
               f"ссылка на вебинар {knowledge_assesment[1]}." if knowledge_assesment is not None else ""}")
# </editor-fold>

# <editor-fold desc="Add school grade">
def get_get_school_grade_grade_text() -> str:
    """Text prompt for adding a new school grade.
    
    :return: The grade input prompt text
    """
    return "Введите номер класса, который хотите добавить."
# </editor-fold>

# <editor-fold desc="Add question">
def get_get_question_school_grade_text() -> str:
    """Text prompt for selecting a question's target grade.
    
    :return: The school grade selection prompt text
    """
    return "Выберите класс, к которому относится вопрос."

def get_get_question_description_text() -> str:
    """Text prompt for entering a question description.
    
    :return: The question description input prompt text
    """
    return "Введите формулировку вопроса."

def get_get_count_of_question_answers_text() -> str:
    """Text prompt for specifying the number of answers.
    
    :return: The answer count input prompt text
    """
    return "Введите количество ответов на вопрос."

def get_get_answer_description_text(answer_number: int) -> str:
    """Text prompt for entering an answer description.
    
    :param answer_number: The sequential number of the answer being entered
    :return: The answer description input prompt text
    """
    return f"Введите ответ №{answer_number}."
# </editor-fold>

# <editor-fold desc="Add event">
def get_get_event_year_text() -> str:
    """Text prompt for entering an event's year.
    
    :return: The year input prompt text
    """
    return "Введите год, в который пройдет событие."

def get_get_event_month_text() -> str:
    """Text prompt for entering an event's month.
    
    :return: The month input prompt text
    """
    return "Введите месяц, в который пройдет событие."

def get_get_event_day_text() -> str:
    """Text prompt for entering an event's day.
    
    :return: The day input prompt text
    """
    return "Введите день, в который пройдет событие."

def get_get_event_hour_text() -> str:
    """Text prompt for entering an event's hour.
    
    :return: The hour input prompt text
    """
    return "Введите час, в который пройдет событие."

def get_get_event_minute_text() -> str:
    """Text prompt for entering an event's minute.
    
    :return: The minute input prompt text
    """
    return "Введите минуту, в котоую пройдет событие."

def get_get_event_max_count_of_buyings_text() -> str:
    """Text prompt for entering an event's maximum capacity.
    
    :return: The maximum capacity input prompt text
    """
    return "Введите максимальное число посетителей события."

def get_get_event_price_text() -> str:
    """Text prompt for entering an event's price.
    
    :return: The price input prompt text
    """
    return "Введите цену посещения события."

def get_get_excursion_address_text() -> str:
    """Text prompt for entering an excursion's address.
    
    :return: The address input prompt text
    """
    return "Введите адрес квеста."

def get_get_knowledge_assesment_link_text() -> str:
    """Text prompt for entering a knowledge assessment's webinar link.
    
    :return: The webinar link input prompt text
    """
    return "Введите ссылку на вебинар."
# </editor-fold>


