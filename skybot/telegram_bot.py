from skybot.api import API
import requests
from threading import Thread
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

class TelegramBot():

    def __init__(self, bot_token):
        self.__api = API(requests)
        updater = Updater(token=bot_token)
        dispatcher = updater.dispatcher 
        start_handler = CommandHandler('live', self.send_live)
        dispatcher.add_handler(start_handler)
        updater.start_polling()

    def send_live(self, bot, update):
        print("send live")
        bot.send_message(chat_id=update.message.chat_id, text=self.__api.get_live())