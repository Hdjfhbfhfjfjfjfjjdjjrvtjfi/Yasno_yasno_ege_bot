__all__ = ["router"]
from aiogram import Router
from aiogram.handlers import MessageHandler
from aiogram.filters.command import Command

from tg_bot.filters.commands import add_administrator_command, delete_administrator_command
from tg_bot.models import Administrator
from tg_bot.utils.mixins import CommandMixin

router: Router = Router()


@router.message(Command(commands=[add_administrator_command, delete_administrator_command]))
class AddOrDeleteAdministratorHandler(MessageHandler, CommandMixin):
    async def handle(self) -> None:
        await self.event.delete()
        is_valid_administrator, administrator_id = await self.is_valid_administrator()
        if is_valid_administrator:
            if self.command.command == add_administrator_command.command:
                await Administrator.create_administrator(administrator_id)
            else:
                await (await Administrator.get_administrator_by_id(administrator_id)).delete()

    async def is_valid_administrator(self) -> tuple[bool, int]:
        is_valid = (len(splitted_message := self.event.text.split()) == 2 and
                    splitted_message[1].isdigit() and
                    (administrator := await Administrator.get_administrator_by_id(self.event.chat.id)) is not None and
                    administrator.can_manipulate_administrator_table)
        return is_valid, int(splitted_message[1])

