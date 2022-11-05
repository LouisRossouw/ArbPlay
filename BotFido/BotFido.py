import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Bots", callback_data="-bots-"),
               InlineKeyboardButton("Admin", callback_data="-admin-"),
               InlineKeyboardButton("🎩about", callback_data="-about-", url="https://louisrossouw.com/"))

    return markup


def logs_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 5

    log_dir = f"{os.path.dirname(os.path.dirname(__file__))}/logs"
    for log in os.listdir(log_dir):
        log_check = log.split(".")
        if log_check[1] == "log":
            print(log_check[0])
            markup.add(InlineKeyboardButton(log_check[0], callback_data=f"LOGS_{log_check[0]}"))
    markup.add(InlineKeyboardButton("⬅️Back", callback_data="-back-"))

    return markup


def admin_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("😱Check Logs", callback_data="-Check_Logs-"))
    markup.add(InlineKeyboardButton("🤠Check Data", callback_data="-Check_Data-"))


def data_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(InlineKeyboardButton("Arbitrage_Play", callback_data="DATA_Arbitrage"))
    markup.add(InlineKeyboardButton("DripDrip", callback_data="DATA_DripDrip"))
    markup.add(InlineKeyboardButton("⬅️Back", callback_data="-back-"))

    return markup



def Bots_list_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Arbitrage_Bot", callback_data="BOT_Arbitrage"))
    markup.add(InlineKeyboardButton("DripDrip_Bot", callback_data="BOT_DripDrip"))
    markup.add(InlineKeyboardButton("⬅️Back", callback_data="-back-"))

    return markup


def Bot_functions_markup(botName):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🛑Stop", callback_data=f"STOP_{botName}"))
    markup.add(InlineKeyboardButton("✳️Start", callback_data=f"STOP_{botName}"))
    markup.add(InlineKeyboardButton("⬅️Back", callback_data="-back-"))   

    return markup










@bot.message_handler(func=lambda message: True)
def message_handler(message):

    is_admin = BotUtils.check_usr(bot, ADMIN_ID, TELEBOT_ADMIN_ALIAS, message)
    if is_admin == True:
        bot.send_message(message.chat.id, "Hi, What would you like to do?", reply_markup=startup_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):








# Markup Navigation.
    if call.data == "-admin-":
         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Admin:", reply_markup=logs_markup())       

    if call.data == "-Check_Logs-":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Current Logs:", reply_markup=logs_markup())

    if call.data == "-about-":
        bot.answer_callback_query(call.id, "www.LouisRossouw.com")


    if call.data == "-Check_Data-":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="🤖Bot Data:", reply_markup=data_markup())

    if call.data == "-bots-":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="🤖Bot list:", reply_markup=Bots_list_markup()) 





# Actions.
    if "LOGS_" in call.data:
        requested_logName = str(call.data).replace("LOGS_", "")
        returned_logs = BotUtils.read_logs(requested_logName)
        bot.send_message(chat_id=ADMIN_ID, 
                                allow_sending_without_reply=True, text=str(returned_logs))

    if "DATA_" in call.data:
        requested_dataName = str(call.data).replace("DATA_", "")
        returned_logs = BotUtils.read_data(requested_dataName)
        bot.send_message(chat_id=ADMIN_ID, 
                                allow_sending_without_reply=True, text=str(returned_logs))


    if "BOT_" in call.data:
        requested_botName = str(call.data).replace("BOT_", "")
        updated_text = BotUtils.read_bot_data(requested_botName)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                        text=f"🤖{requested_botName}:\n\nActive:{updated_text}", reply_markup=Bot_functions_markup(requested_botName)) 

    # if "STOP_" in call.data:



    if call.data == "-back-" :
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Current Logs.", reply_markup=startup_markup())




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