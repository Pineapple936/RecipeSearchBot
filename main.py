from asyncio import run
from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
from os import getenv

from app.handlers import *

load_dotenv()

bot = Bot(token=getenv("TOKEN"))
dp = Dispatcher()
dp.include_routers(command_router, text_router, callback_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())
