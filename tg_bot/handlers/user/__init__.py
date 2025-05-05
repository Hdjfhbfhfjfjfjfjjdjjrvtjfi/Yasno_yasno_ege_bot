__all__ = ["routers"]
from aiogram import Router

from .start_and_registration_handlers import router as start_and_registration_router
from .delete_unwanted_text_handlers import router as delete_unwanted_text_router
from .event_buying_handlers import router as event_buying_router
from .knowledge_assesment_test_handlers import router as knowledge_assesment_test_router
from .user_profile_handlers import router as user_profile_router

from tg_bot.middlewares import DataObjectMiddleware
from tg_bot.utils.constants import TEST_RESULT_DATA_ARGUMENT_NAME, USER_DATA_ARGUMENT_NAME

user_data_middleware = DataObjectMiddleware(USER_DATA_ARGUMENT_NAME)
knowledge_assesment_test_data_middleware = DataObjectMiddleware(TEST_RESULT_DATA_ARGUMENT_NAME)

start_and_registration_router.message.middleware(user_data_middleware)
knowledge_assesment_test_router.callback_query.middleware(knowledge_assesment_test_data_middleware)

routers: list[Router] = [start_and_registration_router, event_buying_router, knowledge_assesment_test_router,
                         user_profile_router, delete_unwanted_text_router]