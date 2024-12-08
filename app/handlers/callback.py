from aiogram import Router
from aiogram.types import CallbackQuery

from app.handlers.create_recipe import user_dishes
from app.backend.backend import create_message
from app.keyboards.inlinekeyboards import create_inlinekeyboard

callback_router = Router()

@callback_router.callback_query()
async def callback(callback: CallbackQuery):
    await callback.answer()
    data = list(map(int, callback.data.split()))
    await callback.message.edit_text(create_message(user_dishes[callback.message.chat.id][data[0]]), reply_markup=create_inlinekeyboard(data[0], data[1]))