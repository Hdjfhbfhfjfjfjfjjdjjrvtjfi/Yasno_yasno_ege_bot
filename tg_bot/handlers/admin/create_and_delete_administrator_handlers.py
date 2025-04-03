__all__ = ["router"]
from aiogram import Router
from aiogram.types import Message, BotCommand
from aiogram.filters.command import Command

from tg_bot.filters.commands import add_administrator_command, delete_administrator_command
from tg_bot.models import Administrator

router: Router = Router()


@router.message(Command(commands=[add_administrator_command, delete_administrator_command]))
async def add_or_delete_administrator_handler(message: Message, command: BotCommand) -> None:
    await message.delete()
    administrator = await Administrator.get_administrator_by_id(message.chat.id)
    if ((administrator.can_manipulate_administrator_table and
        len(splitted_message := message.text.split()) == 2) and
        splitted_message[1].isdigit() and
        await Administrator.get_administrator_by_id(message.chat.id) is not None):
        if command.command == add_administrator_command.command:
            await Administrator.create_administrator(message.chat.id)
        else:
            await (await Administrator.get_administrator_by_id(message.chat.id)).delete()


