from aiogram import Router
from aiogram.handlers import MessageHandler


router = Router()

@router.message()
class DeleteUnwantedTextHandler(MessageHandler):
    async def handle(self) -> None:
        await self.event.delete()
