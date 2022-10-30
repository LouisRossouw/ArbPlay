import os
from tokenize import Token
import telebot

BOT_TOKEN = os.getenv("BOTFRIDO_API_KEY")
bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode=None)



