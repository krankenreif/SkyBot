from skybot.api import API
import requests
from threading import Thread
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, ConversationHandler, MessageHandler, Filters
from telegram import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, Bot, Update

class TelegramBot():

    CLUB, PILOT = range(2)

    def __init__(self, bot_token):
        self.__api = API(requests)
        updater = Updater(token=bot_token)
        dispatcher = updater.dispatcher 
        live_handler = CommandHandler(command='live', callback=self.send_live)
        add_handler = CommandHandler(command='add', callback=self.add)    
        dispatcher.add_handler(CallbackQueryHandler(self.add_pilot, pattern='add_pilot'))

        club_add_handler = ConversationHandler( entry_points=[CallbackQueryHandler(callback=self.add_club, pattern='add_club')],
                                                states={TelegramBot.CLUB: [MessageHandler(filters=Filters.regex("^\d+$"), callback=self.club_answer)]},
                                                fallbacks=[CommandHandler(command='cancel', callback=self.cancel)])
        dispatcher.add_handler(live_handler)
        dispatcher.add_handler(add_handler)
        dispatcher.add_handler(club_add_handler)
        updater.start_polling()
        updater.idle()

    def send_live(self, bot: Bot, update: Update):
        print("send live")
        bot.send_message(chat_id=update.message.chat_id, text=self.__api.get_live())

    def add(self, bot: Bot, update: Update):
        print("add")
        keyboard = [[InlineKeyboardButton(text='pilot', callback_data="add_pilot")],
            [InlineKeyboardButton(text='club', callback_data="add_club")]]
        bot.send_message(chat_id=update.message.chat_id, text="Select what to add", reply_markup=InlineKeyboardMarkup(keyboard))
        
    def add_club(self, bot: Bot, update: Update):
        print("add club")
        query = update.callback_query
        club_ask = bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Please enter club number (only numbers allowed)")
        return TelegramBot.CLUB

    def club_answer(self, bot: Bot, update: Update):
        update.message.reply_text(f"Club {update.message.text}")
        return ConversationHandler.END

    def add_pilot(self, bot, update):
        print("add pilot")

    def add_keyboard():
        keyboard = [[KeyboardButton('pilot', callback_data='add_pilot')],
            [KeyboardButton('club', callback_data='add_club')]]
        return ReplyKeyboardMarkup(keyboard)

    def cancel(update, context):
        print(update.message.from_user)
        update.message.reply_text('Bye! I hope we can talk again some day.')
        return ConversationHandler.END