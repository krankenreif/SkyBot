from skybot.api import API
import requests
from threading import Thread
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, ConversationHandler, MessageHandler, Filters
from telegram import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, Bot, Update

class TelegramBot():

    CLUB, PILOT = range(2)

    def __init__(self, bot_token):
        self.__api = API(requests)
        self.__updater = Updater(token=bot_token)
        self.__dispatcher = self.__updater.dispatcher 
        self.__live_handler = CommandHandler(command='live', callback=self.send_live)
        self.__menu_handler = CommandHandler(command='menu', callback=self.main_menu)
        self.__add_handler = CallbackQueryHandler(pattern='add', callback=self.add)
        self.__remove_handler = CallbackQueryHandler(pattern='remove', callback=self.remove)
        self.__add_club_handler = CallbackQueryHandler(pattern='club_add', callback=self.add_club)
        self.__add_pilot_handler = CallbackQueryHandler(pattern='pilot_add', callback=self.add_pilot)
        self.__add_back_handler = CallbackQueryHandler(pattern='back_add', callback=self.add_back)
        self.__retrieve_club_number_handler = MessageHandler(filters=Filters.text, callback=self.retrieve_club_number)
        self.__retrieve_pilot_number_handler = MessageHandler(filters=Filters.text, callback=self.retrieve_pilot_number)
        self.__dispatcher.add_handler(self.__live_handler)
        self.__dispatcher.add_handler(self.__menu_handler)
        self.__dispatcher.add_handler(self.__add_handler)
        self.__dispatcher.add_handler(self.__remove_handler)
        self.__dispatcher.add_handler(self.__add_club_handler)
        self.__dispatcher.add_handler(self.__add_pilot_handler)
        self.__dispatcher.add_handler(self.__add_back_handler)
        self.__updater.start_polling()
        self.__updater.idle()

    def send_live(self, bot: Bot, update: Update):
        print("send live")
        bot.send_message(chat_id=update.message.chat_id, text=self.__api.get_live())

    def main_menu(self, bot: Bot, update: Update, with_history=False):
        keyboard = [[InlineKeyboardButton(text='Add', callback_data="add"), InlineKeyboardButton(text='Remove', callback_data="remove")]]
        if not with_history:
            bot.send_message(chat_id=update.message.chat_id, text="What do you want to do?", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            print("open menu with history")
            query = update.callback_query
            bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="What do you want to do?", reply_markup=InlineKeyboardMarkup(keyboard))

    def add(self, bot: Bot, update: Update, message=""):
        print("add ")
        keyboard = [[InlineKeyboardButton(text='pilot', callback_data="pilot_add"), InlineKeyboardButton(text='club', callback_data="club_add")],[InlineKeyboardButton(text='<< Back to menu', callback_data="back_add")]]
        query = update.callback_query
        if message != "":
            bot.send_message(chat_id=update.message.chat_id, text="Select what to add", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message + "\nSelect what to add", reply_markup=InlineKeyboardMarkup(keyboard))

    def remove(self, bot: Bot, update: Update, message=""):
        print("remove")
        #keyboard = [[InlineKeyboardButton(text='pilot', callback_data="add_pilot"), InlineKeyboardButton(text='club', callback_data="add_club")],[InlineKeyboardButton(text='<< Back to menu', callback_data="add_back")]]
        #bot.send_message(chat_id=update.message.chat_id, text=message + "\nSelect what to add", reply_markup=InlineKeyboardMarkup(keyboard))
        
    def add_club(self, bot: Bot, update: Update):
        print("add club")
        query = update.callback_query
        club_ask = bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Please enter club number (only numbers allowed)")
        self.__dispatcher.add_handler(self.__retrieve_club_number_handler)

    def add_pilot(self, bot: Bot, update: Update):
        print("add pilot")
        query = update.callback_query
        pilot_ask = bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Please enter pilot number (only numbers allowed)")
        self.__dispatcher.add_handler(self.__retrieve_pilot_number_handler)

    def retrieve_club_number(self, bot: Bot, update: Update):
        print("retrieved club number " + update.message.text)
        self.__dispatcher.remove_handler(self.__retrieve_club_number_handler)
        self.add(bot=bot, update=update, message=f"Club {update.message.text} added")

    def retrieve_pilot_number(self, bot: Bot, update: Update):
        print("retrieved pilot number " + update.message.text)
        self.__dispatcher.remove_handler(self.__retrieve_pilot_number_handler)
        self.add(bot=bot, update=update, message=f"Pilot {update.message.text} added")
    
    def add_back(self, bot: Bot, update: Update):
        self.main_menu(bot=bot, update=update, with_history=True)