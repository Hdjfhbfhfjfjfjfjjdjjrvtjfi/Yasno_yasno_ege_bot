__all__ = ["routers"]
from aiogram import Router

from .create_and_delete_administrator_handlers import router as create_and_delete_administrator_router
from .get_database_handlers import router  as get_database_router
from .add_school_grade_handlers import router as add_school_grade_router
from .add_question_handlers import router as add_question_router
from .add_event_handlers import router as add_event_router

from tg_bot.middlewares import CheckAdministratorRightsMiddleware, DataObjectMiddleware
from tg_bot.utils.constants import SCHOOL_GRADE_DATA_ARGUMENT_NAME, QUESTION_DATA_ARGUMENT_NAME, \
    EVENT_DATA_ARGUMENT_NAME

check_administrator_rights_middleware = CheckAdministratorRightsMiddleware()
school_grade_data_middleware = DataObjectMiddleware(SCHOOL_GRADE_DATA_ARGUMENT_NAME)
question_data_middleware = DataObjectMiddleware(QUESTION_DATA_ARGUMENT_NAME)
event_data_middleware = DataObjectMiddleware(EVENT_DATA_ARGUMENT_NAME)

add_school_grade_router.message.middleware(school_grade_data_middleware)
add_question_router.message.middleware(question_data_middleware)
add_question_router.callback_query.middleware(question_data_middleware)
add_event_router.message.middleware(event_data_middleware)

routers: list[Router] = [create_and_delete_administrator_router, get_database_router, add_school_grade_router,
                         add_question_router, add_event_router]

for router in routers:
    router.message.middleware(check_administrator_rights_middleware)