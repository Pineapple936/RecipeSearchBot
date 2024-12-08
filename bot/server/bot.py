from bot.server.backend import *
import telebot
from telebot import types

class Bot:
    def __init__(self, token):
        self.__token = token
        self.__bot = telebot.TeleBot(self.__token)
        self.__user_dishes = dict()
        self.__last_bot_message = dict()
        self.__symbol_previous = "←"
        self.__symbol_next = "→"

    def run(self):
        @self.__bot.message_handler(commands=["start"])
        def __start(message):
            self.__bot.send_message(message.chat.id, "Добро пожаловать в мир кулинарного вдохновения! Поделись со мной своими любимыми ингредиентами, и я помогу тебе создать настоящие гастрономические шедевры. Начнем наше кулинарное путешествие?")

        @self.__bot.message_handler(commands=["help"])
        def __help(message):
            self.__bot.send_message(message.chat.id, """Добро пожаловать! Я здесь, чтобы помочь тебе найти вкусные рецепты и вдохновиться новыми идеями для приготовления пищи.\n\nВот что я умею делать:
/start – начнем наше кулинарное путешествие вместе!\n/help – вернись к этому сообщению помощи в любое время.\n\nПросто начни писать игридиенты, чтобы я отправил тебе кулинарный рецепт""")

        @self.__bot.message_handler(content_types=["text"])
        def __search(message):
            if message.chat.id in self.__last_bot_message:
                self.__delete_old_markup(self.__last_bot_message[message.chat.id])
                self.__last_bot_message.pop(message.chat.id)
            dishes = search_recipes(message.text)
            if dishes["responce"] == 200:
                self.__user_dishes[message.from_user.id] = dishes["content"]
                markup = self.__create_markup(len(dishes["content"]) - 1)
                last_message = self.__bot.send_message(message.chat.id, create_message(dishes["content"][0]), reply_markup=markup)
                if len(dishes["content"]) != 1:
                    self.__last_bot_message[last_message.chat.id] = last_message
            else:
                self.__bot.send_message(message.chat.id, dishes["content"])
                if message.from_user.id in self.__user_dishes:
                    self.__user_dishes.pop(message.from_user.id)

        @self.__bot.callback_query_handler(func=lambda call: True)
        def callback_data(call):
            data = call.data.split()
            markup = self.__create_markup(int(data[0]), int(data[1]))
            self.__bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, 
                                         text=create_message(self.__user_dishes[call.from_user.id][int(data[1])]), reply_markup=markup)

        self.__bot.infinity_polling()

    def __create_markup(self, max_indx: int, indx=0):
        if max_indx != 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            if indx == 0:
                btn_next = types.InlineKeyboardButton(text=self.__symbol_next, callback_data=f"{max_indx} {indx + 1}")
                markup.add(btn_next)
            elif indx == max_indx:
                btn_previous = types.InlineKeyboardButton(text=self.__symbol_previous, callback_data=f"{max_indx} {indx - 1}")
                markup.add(btn_previous)
            else:
                btn_next = types.InlineKeyboardButton(text=self.__symbol_next, callback_data=f"{max_indx} {indx + 1}")
                btn_previous = types.InlineKeyboardButton(text=self.__symbol_previous, callback_data=f"{max_indx} {indx - 1}")
                markup.add(btn_previous, btn_next)
        else:
            markup = None
        return markup

    def __delete_old_markup(self, message: telebot.types.Message):
        self.__bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.id, reply_markup=None)
