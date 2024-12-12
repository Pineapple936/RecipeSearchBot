from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.message_text.text import *

command_router = Router()

@command_router.message(CommandStart())
async def start(message: Message):
    await message.answer(text_start)

@command_router.message(Command("help"))
async def help(message: Message):
    await message.answer(text_help)