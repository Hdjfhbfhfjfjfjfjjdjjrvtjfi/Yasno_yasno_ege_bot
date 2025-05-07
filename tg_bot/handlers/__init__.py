__all__ = ["routers"]
from aiogram import Router

from .admin import routers as admin_routers
from .user import routers as user_routers

routers: list[Router] = admin_routers + user_routers