import telebot
import config

bot = telebot.TeleBot(config.telegram_token, parse_mode='MARKDOWN', threaded=False)
