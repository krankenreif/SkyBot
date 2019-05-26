import sys
import logging

# local imports
from skybot.telegram_bot import TelegramBot

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    cmd_arguments = sys.argv[1:]
    if len(cmd_arguments) >= 2:
        if cmd_arguments[0] == "-telegram":
            bot = TelegramBot(bot_token=cmd_arguments[1])
        else:
            print("1. argument has to be -telegram")
    else:
        print("two arguments required")

if __name__ == "__main__":
    main()