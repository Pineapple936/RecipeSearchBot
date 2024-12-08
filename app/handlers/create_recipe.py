from aiogram import Router, F
from aiogram.types import Message

from app.backend.backend import create_message, search_recipes
from app.keyboards.inlinekeyboards import create_inlinekeyboard

text_router = Router()
user_dishes = dict()
last_bot_message = dict()

@text_router.message(F.text)
async def recipe(message: Message):
    if message.chat.id in last_bot_message:
        await last_bot_message[message.chat.id].delete_reply_markup()
        last_bot_message.pop(message.chat.id)

    recipes = search_recipes(message.text)
    if recipes["responce"] == 200:
        user_dishes[message.chat.id] = recipes["content"]
        bot_message = await message.answer(create_message(recipes["content"][0]), reply_markup=create_inlinekeyboard(0, len(recipes["content"]) - 1))

        if len(recipes["content"]) != 1:
            last_bot_message[message.chat.id] = bot_message

    else:
        await message.answer(recipes["content"])

        if message.chat.id in user_dishes:
            user_dishes.pop(message.chat.id)
