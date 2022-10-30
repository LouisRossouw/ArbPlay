
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

        text_line_1 = 'WARNING: \n\n* Unrecognized user interacted with TurtleTurtle *'
        text_line_2 = '\n\nUSR Details:'
        text_line_3 = '\n\nusr_name: ' + str(usr_name) + '\nusr_surname: ' + str(usr_surname) + '\nusr_nickname: ' + str(usr_user_name)
        text_line_4 = '\n\nusr_id: ' + str(usr_id) + '\nusr_is_bot: ' + str(usr_is_bot) + '\nusr_language: ' + str(usr_language) + '\n\nusr_content_type: ' + str(usr_content_type) + '\nText: ' + str(usr_text)

        # To Admin / Owner of TurtleTurtle
        text_msg = text_line_1 + text_line_2 + text_line_3 + text_line_4
        bot.send_message(chat_id=ADMIN_ID, allow_sending_without_reply=True, text=text_msg)

        # To Un-Authorized USER
        text_warning = str(usr_name) + '_' + str(usr_surname) + '\n\n .. \n\nYou are not authorized to use this Bot'
        bot.send_message(chat_id=usr_id, allow_sending_without_reply=True, text=text_warning)

    elif IS_ADMIN == True:
        pass

    return IS_ADMIN