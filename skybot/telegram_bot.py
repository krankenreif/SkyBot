from skybot.api import API
from skybot.user_database import UserDatabase
import requests
from threading import Thread
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, ConversationHandler, MessageHandler, Filters
from telegram import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, Bot, Update

class TelegramBot():

    CLUB, PILOT = range(2)

    def __init__(self, bot_token):
        self.__api = API(requests)
        self.__user_database = UserDatabase()
        self.__updater = Updater(token=bot_token)
        self.__dispatcher = self.__updater.dispatcher 
        self.__live_handler = CommandHandler(command='live', callback=self.send_live)
        self.__menu_handler = CommandHandler(command='menu', callback=self.main_menu)
        self.__add_handler = CallbackQueryHandler(pattern='add', callback=self.add)
        self.__remove_handler = CallbackQueryHandler(pattern='remove', callback=self.remove)
        self.__add_club_handler = CallbackQueryHandler(pattern='club_add', callback=self.add_club)
        self.__add_pilot_handler = CallbackQueryHandler(pattern='pilot_add', callback=self.add_pilot)
        self.__add_back_handler = CallbackQueryHandler(pattern='back_add', callback=self.add_back)
        self.__cancel_handler = CallbackQueryHandler(pattern='cancel', callback=self.cancel)
        self.__cancel_keyboard = [[InlineKeyboardButton(text='cancel', callback_data="cancel")]]
        self.__retrieve_club_number_handler = MessageHandler(filters=Filters.text, callback=self.retrieve_club_number)
        self.__retrieve_pilot_number_handler = MessageHandler(filters=Filters.text, callback=self.retrieve_pilot_number)
        self.__dispatcher.add_handler(self.__add_handler)
        self.__dispatcher.add_handler(self.__remove_handler)
        self.__dispatcher.add_handler(self.__add_club_handler)
        self.__dispatcher.add_handler(self.__add_pilot_handler)
        self.__dispatcher.add_handler(self.__add_back_handler)
        self.__dispatcher.add_handler(self.__cancel_handler)
        self.enable_handlers()
        self.__updater.start_polling()
        self.__updater.idle()

    def send_live(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text=self.__api.get_live())

    def main_menu(self, bot: Bot, update: Update, with_history=False):
        self.disable_handlers()
        keyboard = [[InlineKeyboardButton(text='Add', callback_data="add"), InlineKeyboardButton(text='Remove', callback_data="remove")]]
        if not with_history:
            bot.send_message(chat_id=update.message.chat_id, text="What do you want to do?", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            query = update.callback_query
            bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="What do you want to do?", reply_markup=InlineKeyboardMarkup(keyboard))

    def add(self, bot: Bot, update: Update, message=""):
        keyboard = [[InlineKeyboardButton(text='pilot', callback_data="pilot_add"), InlineKeyboardButton(text='club', callback_data="club_add")],[InlineKeyboardButton(text='<< Back to menu', callback_data="back_add")]]
        query = update.callback_query
        if message != "":
            if query:
                bot.send_message(chat_id=query.message.chat_id, text=message + "\nSelect what to add", reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                bot.send_message(chat_id=update.message.chat.id, text=message + "\nSelect what to add", reply_markup=InlineKeyboardMarkup(keyboard)) 
        else:
            bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Select what to add", reply_markup=InlineKeyboardMarkup(keyboard))

    def remove(self, bot: Bot, update: Update, message=""):
        query = update.callback_query
        self.add(bot=bot, update=update, message=f"Club {str(self.__user_database.get_monitored(telegram_id=int(query.message.chat.id)))} removed")
        
    def add_club(self, bot: Bot, update: Update):
        query = update.callback_query
        club_ask = bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Please enter club number (only numbers allowed)", reply_markup=InlineKeyboardMarkup(self.__cancel_keyboard))
        self.__dispatcher.add_handler(self.__retrieve_club_number_handler)

    def add_pilot(self, bot: Bot, update: Update):
        query = update.callback_query
        pilot_ask = bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Please enter pilot number (only numbers allowed)", reply_markup=InlineKeyboardMarkup(self.__cancel_keyboard))
        self.__dispatcher.add_handler(self.__retrieve_pilot_number_handler)

    def retrieve_club_number(self, bot: Bot, update: Update):
        if not str.isnumeric(update.message.text):
            bot.send_message(chat_id=update.message.chat_id, text="Enter a number you twat!", reply_markup=InlineKeyboardMarkup(self.__cancel_keyboard))
            return
        for pilot_id in self.__api.get_pilots(update.message.text):
            self.__user_database.add_user(telegram_id=int(update.message.chat.id), user_id=int(pilot_id))
        self.__dispatcher.remove_handler(self.__retrieve_club_number_handler)
        self.add(bot=bot, update=update, message=f"Club {update.message.text} added")

    def retrieve_pilot_number(self, bot: Bot, update: Update):
        if not str.isnumeric(update.message.text):
            bot.send_message(chat_id=update.message.chat_id, text="Enter a number you twat!", reply_markup=InlineKeyboardMarkup(self.__cancel_keyboard))
            return
        self.__user_database.add_user(telegram_id=int(update.message.chat.id), user_id=update.message.text)
        self.__dispatcher.remove_handler(self.__retrieve_pilot_number_handler)
        self.add(bot=bot, update=update, message=f"Pilot {update.message.text} added")
    
    def add_back(self, bot: Bot, update: Update):
        self.main_menu(bot=bot, update=update, with_history=True)

    def cancel(self, bot: Bot, update: Update):
        self.enable_handlers()
        self.__dispatcher.remove_handler(self.__retrieve_club_number_handler)
        self.__dispatcher.remove_handler(self.__retrieve_pilot_number_handler)
        bot.edit_message_text(chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id, text="Canceled")

    def disable_handlers(self):
        self.__dispatcher.remove_handler(self.__menu_handler)
        self.__dispatcher.remove_handler(self.__live_handler)

    def enable_handlers(self):
        self.__dispatcher.add_handler(self.__live_handler)
        self.__dispatcher.add_handler(self.__menu_handler)