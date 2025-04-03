from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def delete_unwanted_text_handler(message: Message) -> None:
    await message.delete()
