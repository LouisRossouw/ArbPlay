import os
import sys
from telnetlib import SE

import telebot

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Settings



class BotNotification():
    """ Basic Notification class for Telebot. """

    def __init__(self):
        """ initialize. """

        BOT_TOKEN = os.getenv("BOTFRIDO_API_KEY")
        TELEBOT_ADMIN_ALIAS = os.getenv("TELEBOT_ADMIN_ALIAS")
        self.bot = telebot.TeleBot(BOT_TOKEN)

        self.ADMIN_ID = TELEBOT_ADMIN_ALIAS.split("-")[3]

        self.SETTINGS = Settings.Settings()
        self.notifications = self.SETTINGS.Notifications




    def send_ADMIN_notification(self, text):
        """ Send notification to Admin ID """

        if self.notifications == True:

            self.bot.send_message(chat_id=self.ADMIN_ID, 
                                  allow_sending_without_reply=True, 
                                  text=str(text))





if __name__ == "__main__":

    BotNot = BotNotification()
    BotNot.send_notification("TESTING")