__all__ = ["router"]
from aiogram import Router, Bot
from aiogram.filters.command import Command
from aiogram.types import Message, BufferedInputFile

from io import BytesIO

from tg_bot.filters.commands import get_database_command
from tg_bot.models import (Administrator, BotUserProfile, Excursion, KnowledgeAssesment, Order, SchoolGrade, TestAnswer,
                           TestQuestion, TestResponse, TestResult, User)
from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.visitors.xlsx_visitor import XLSXVisitor


router: Router = Router()


@router.message(Command(commands=[get_database_command]))
async def get_database_handler(message: Message, bot: Bot) -> None:
    await message.delete()
    export_visitor = XLSXVisitor()
    models: list[type[ICanAcceptVisitor]] = [Administrator, BotUserProfile, Excursion, KnowledgeAssesment, Order, SchoolGrade, TestAnswer,
              TestQuestion, TestResponse, TestResult, User]
    for model in models:
        await model.accept(export_visitor)
    file: BytesIO = BytesIO()
    export_visitor.workbook.save(file)
    await bot.send_document(
        chat_id=message.chat.id,
        document=BufferedInputFile(file.getvalue(), "database.xlsx")
    )
