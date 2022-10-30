import os

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import BotUtils

BOT_TOKEN = os.getenv("BOTFRIDO_API_KEY")
TELEBOT_ADMIN_ALIAS = os.getenv("TELEBOT_ADMIN_ALIAS")
ADMIN_ID = TELEBOT_ADMIN_ALIAS.split("-")[3]

bot = telebot.TeleBot(BOT_TOKEN)



def keyboard(key_type="Normal"):

    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton("✅"))

    return markup


def startup_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton("Check Logs", callback_data="-Check_Logs-"),
               InlineKeyboardButton("Check Data", callback_data="-Check_Data-", url="https://louisrossouw.com/"))

    return markup






@bot.message_handler(func=lambda message: True)
def message_handler(message):

    is_admin = BotUtils.check_usr(bot, ADMIN_ID, TELEBOT_ADMIN_ALIAS, message)
    if is_admin == True:
        bot.send_message(message.chat.id, "Hi, What would you like to do?", reply_markup=startup_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "-Check_Logs-":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "-Check_Data-":
        bot.answer_callback_query(call.id, "Answer is No")










@bot.message_handler(commands=["start"])
def start_message(message):

    bot.send_message(message.chat.id,
                     text="Hello", 
                     reply_markup=keyboard())



@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if message.text == "✅":

        markup = telebot.types.ReplyKeyboardRemove()

        bot.send_message(message.from_user.id, 
                        text="Done with Keyboard",
                        reply_markup=markup)




bot.infinity_polling()