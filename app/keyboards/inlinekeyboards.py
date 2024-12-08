from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inlinekeyboard(indx, max_indx):
    if max_indx != 0:
        markup = InlineKeyboardBuilder()
        if indx == 0:
            markup.add(InlineKeyboardButton(text="→", callback_data=f"{indx + 1} {max_indx}"))
        elif indx == max_indx:
            markup.add(InlineKeyboardButton(text="←", callback_data=f"{indx - 1} {max_indx}"))
        else:
            markup.add(InlineKeyboardButton(text="←", callback_data=f"{indx - 1} {max_indx}"))
            markup.add(InlineKeyboardButton(text="→", callback_data=f"{indx + 1} {max_indx}"))
        return markup.as_markup()
