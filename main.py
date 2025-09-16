# Updated bot without language selection (can be added later)
# Requires: pip install pyTelegramBotAPI, requests
import telebot
import config
from handlers.menu import register_menu_handlers
from handlers.courses import register_course_handlers
from handlers.support import register_support_handlers
from handlers.fileid import register_fileid_handler

bot = telebot.TeleBot(config.API_TOKEN)

register_menu_handlers(bot)
register_course_handlers(bot)
register_support_handlers(bot)
register_fileid_handler(bot)

if __name__ == "__main__":
    print("🤖 Bot running...")
    bot.infinity_polling()