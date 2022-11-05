import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import toolUtils.utils as utils
import notification_format



def read_bot_data(requested_botName):
    """ Returns data for bot. """

    if requested_botName == "DripDrip":
        data_path = f"{os.path.dirname(os.path.dirname(__file__))}/DripDrip/data/drip_data.json"
    if requested_botName == "Arbitrage":
        data_path = f"{os.path.dirname(os.path.dirname(__file__))}/ArbitragePlay/data/arbitrage.json"

    json_data = utils.read_json(data_path)
    
    return json_data




def read_data(requested_dataName):
    """ Returns data for bot. """

    if requested_dataName == "DripDrip":
        data_path = f"{os.path.dirname(os.path.dirname(__file__))}/DripDrip/data/drip_data.json"
    if requested_dataName == "Arbitrage":
        data_path = f"{os.path.dirname(os.path.dirname(__file__))}/ArbitragePlay/data/arbitrage.json"

    json_data = utils.read_json(data_path)
    reformatted = notification_format.data_format(json_data, requested_dataName)

    return reformatted



def read_logs(logname):
    """ Returns logs. """

    lines = []
    log_file = f"{os.path.dirname(os.path.dirname(__file__))}/logs/{logname}.log"

    with open(log_file, 'r') as f:
        for line in f:
            lines.append(line)

    reformatted = notification_format.logs_format(lines[-15:], logname)

    return reformatted




def check_usr(bot, 
              ADMIN_ID, 
              TELEBOT_ADMIN_ALIAS, message):

    """ Checks if the user is Admin. """
    usr_name = message.from_user.first_name
    usr_surname = message.from_user.last_name
    usr_user_name = message.from_user.username     

    usr_id = message.from_user.id
    usr_is_bot = message.from_user.is_bot

    usr_language = message.from_user.language_code
    usr_content_type = message.content_type
    usr_text = message.text

    user_full_alias = f"{usr_name}-{usr_surname}-{usr_user_name}-{str(usr_id)}"

    if user_full_alias != TELEBOT_ADMIN_ALIAS:
        IS_ADMIN = False

    if user_full_alias == TELEBOT_ADMIN_ALIAS:
        IS_ADMIN = True

    if IS_ADMIN != True:

        admin_False(bot, usr_name, 
                    usr_surname, usr_user_name, 
                    usr_id, usr_is_bot, usr_language, 
                    usr_content_type, usr_text, ADMIN_ID)

    elif IS_ADMIN == True:
        pass

    return IS_ADMIN




def admin_False(bot, usr_name, 
                usr_surname, usr_user_name, 
                usr_id, usr_is_bot, usr_language, 
                usr_content_type, usr_text, ADMIN_ID):

    """ If Admin != False run this function. """

    txt1 = 'WARNING: \n\n* Unrecognized user interacted with TurtleTurtle *'
    txt2 = '\n\nUSR Details:'
    txt3 = '\n\nusr_name: ' + str(usr_name) + '\nusr_surname: '
    txt4 = str(usr_surname) + '\nusr_nickname: ' + str(usr_user_name)
    txt5 = '\n\nusr_id: ' + str(usr_id) + '\nusr_is_bot: ' + str(usr_is_bot) + '\nusr_language: '
    txt6 = str(usr_language) + '\n\nusr_content_type: ' + str(usr_content_type) + '\nText: ' + str(usr_text)

    # To Admin / Owner of TurtleTurtle
    text_msg = txt1 + txt2 + txt3 + txt4 + txt5 + txt6
    bot.send_message(chat_id=ADMIN_ID, 
                     allow_sending_without_reply=True, text=text_msg)

    # To Un-Authorized USER
    txt_warning1 = str(usr_name) + '_' + str(usr_surname)
    txt_warning2 = '\n\n .. \n\nYou are not authorized to use this Bot'
    bot.send_message(chat_id=usr_id, 
                    allow_sending_without_reply=True, text=txt_warning1+txt_warning2)


if __name__ == "__main__":

    read_logs("DripLogs")
