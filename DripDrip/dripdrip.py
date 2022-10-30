import os
import sys
import random
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Settings
import notification_format as N_txtFormat
import toolUtils.utils as utils
import toolUtils.logger as LOG
import Exchanges.valr_exchange as VALR

import BotFido.BotNotifications as BotNot


class DripDrip():
    """ A class for the drip system. """

    def __init__(self):
        """ Initialize drip. """

        self.SETTINGS = Settings.Settings()
        self.VALR_EXCHANGE = VALR.Valr()
        self.LOGLOG = LOG.LogLog().DripLog()
        self.BOTNOT = BotNot.BotNotification()

        self.days = self.SETTINGS.days
        self.invest_time = self.SETTINGS.invest_time # first 2 digits of a digital watch.
        self.drip_data_path = f"{os.path.dirname(os.path.abspath(__file__))}/data/drip_data.json"

        self.data = self.SETTINGS.drip_invest

        self.LOGLOG.info("Drip Initialized.")
        





    def get_dripData(self, key_name):
        """ Generic get data from drip_data.json. """   

        drip_data = utils.read_json(self.drip_data_path)
        return drip_data[key_name]




    def set_dripData(self, key_name, data):
        """ Generic set data to drip_data.json. """
        
        drip_data = utils.read_json(self.drip_data_path)
        drip_data[key_name] = data
        utils.write_to_json(self.drip_data_path, drip_data)




    def calculate_plan(self, amount_capital):
        """ calculates the amount it must invest for each coin over the amount of days, 
            and sets it in the data. """

        self.LOGLOG.info(f"adding new Calculated plan:")

        my_data = self.data

        coins = []
        coin_values = []

        for data in my_data:
            value = my_data[data]

            coins.append(data)
            coin_values.append(value)

        randomList = random.choices(coins, 
                                    weights=coin_values, 
                                    k=int(float(amount_capital)))

        data = {}
        total = []
        
        for i in coins:

            coin_amount = randomList.count(i)
            total.append(coin_amount)

            round_down = utils.round_down_float(coin_amount / self.days)
            data[i] = round_down

            self.LOGLOG.info(f"{i}: {str(round_down)}")

        # Reset
        self._set_CALCULATE_data(data=data)

        # # TeleGram Notification
        calc_txtFormat = N_txtFormat.calculation_format(data, total, amount_capital, self.days)
        self.BOTNOT.send_ADMIN_notification(text=calc_txtFormat)





    def invested_today(self):
        """ Check if it is a new day, if True, execute trade. """

        # compare the last investment date with the date now.
        invested_date = self.get_dripData(key_name="last_invested_date")
        todays_date = utils.get_dates()[0]

        if todays_date == invested_date:
            Invested_today = True
        else:
            Invested_today = False
            self.set_dripData(key_name="already_invested", data=False)

        return Invested_today




    def buy_coins(self, drip_data):
        """ Execute multiple buys for coin in coin list and its amount. """

        plan = drip_data["plan"]

        for coin in plan:

            amount = plan[coin]
        
            valr_sub_acc = self.SETTINGS.valr_DripDrip_acc_name
            acc_ID = self.VALR_EXCHANGE.get_account_ID(acc_label=valr_sub_acc)

            market_data = self.VALR_EXCHANGE.Valr_client.get_market_summary()
            coin_askPrice = self.VALR_EXCHANGE.return_coinPair_data(coinpair=coin+"ZAR", 
                                                                    market_data=market_data)["askPrice"]

            amount_coins_buy = float(float(amount) / float(coin_askPrice))
            # round_down_coin_amount = utils.round_down_float(amount_coins_buy)

            self.LOGLOG.info(f"Buy: {str(coin)} - {str(amount_coins_buy)} | R {str(amount)}")
            print("Buy:", str(coin) + " - ", str(amount_coins_buy), "| R" + str(amount))

            self.VALR_EXCHANGE.subAcc_BUY_ZAR_to_coin(amount_in_coins=amount_coins_buy, 
                                                      coin_pair=coin + "ZAR", 
                                                      sub_ID=acc_ID)

            # TeleGram Notification
            calc_txtFormat = N_txtFormat.buy_format(drip_data, coin, amount_coins_buy, amount)
            self.BOTNOT.send_ADMIN_notification(text=calc_txtFormat)

            sleep(5)

        # Get Summary
        self.total_value()




    def total_value(self):
        """ calculates total value of current Drip account. """

        drip_data = utils.read_json(self.drip_data_path)

        valr_sub_acc = self.SETTINGS.valr_DripDrip_acc_name
        acc_ID = self.VALR_EXCHANGE.get_account_ID(acc_label=valr_sub_acc)

        balances = self.VALR_EXCHANGE.get_balances(acc_ID=acc_ID, account_type="sub")
        market_data = self.VALR_EXCHANGE.Valr_client.get_market_summary()
        plan = drip_data["plan"]

        count_value = []

        txt = ""
        for plan_currency in plan:

            for i in balances:
                currency = i["currency"]
                available = i["available"]


                if plan_currency == currency:
                    askPrice = self.VALR_EXCHANGE.return_coinPair_data(coinpair=currency + "ZAR", market_data=market_data)["askPrice"]
                    calculate_to_ZAR = round(float(available) * float(askPrice),3)

                    txt += f"\n🔹{currency} : {str(round(float(available),5))} R{str(askPrice)} R{str(calculate_to_ZAR)}"
                    count_value.append(calculate_to_ZAR)
                    
                elif "ZAR" == currency:
                    ZAR_available = i["available"]

        total_sum = round(sum(count_value),2)
        percentage = utils.get_percentage_difference(total_sum, 5000)
        formatted_txt = f"💎💎 DripDrip Summary: \n{txt}\n\nTotal R{str(total_sum)} / {str(round(percentage,1))}%"
        self.BOTNOT.send_ADMIN_notification(text=formatted_txt)




    def run(self):
        """ Runs drip. """

        try:
            self.run_algo()
        except Exception as e:
            print(e)
            self.LOGLOG.error(e)
            sleep(10)




    def run_algo(self):
        """ Runs drip. """

        # Check if its a new day, if True, execute trade.
        invested_today = self.invested_today()
        print("invested_today:", invested_today)

        if invested_today == False:
            active = self.get_dripData(key_name="active") 

            # if have not reached total days investing, then buy.
            if active != False:

                # Collect data
                drip_data = utils.read_json(self.drip_data_path)
                time_now = utils.get_dates()[1].split(":")[0] # get first hour only

                # If time is now, then invest
                if int(time_now) == self.invest_time:
                    print("time is golden")

                    if drip_data["already_invested"] != True:
                        print("have not invested - lets invest now!")
                        self.LOGLOG.info("Buying coins.")

                        self.buy_coins(drip_data)

                        day_count = int(self.get_dripData(key_name="day_count"))

                        self.set_dripData(key_name="already_invested", data=True)
                        self.set_dripData(key_name="last_invested_date", data=utils.get_dates()[0])
                        self.set_dripData(key_name="day_count", data=day_count + 1)

                        total_days = self.get_dripData(key_name="days_total")

                        if int(day_count + 1) == int(total_days):
                            print("Done")

                            self.LOGLOG.info(f"Completed Drip: {str(day_count + 1)} / {str(total_days)}")
                            self.set_dripData(key_name="active", data=False)      
            else:
                print("Not active - deposit ZAR to activate bot.")
                enough_funds = self.check_ZAR()

                if enough_funds[0] == True:
                    self.calculate_plan(amount_capital=enough_funds[1])




    def check_ZAR(self):
        """ Checks if ZAR balance more than, 
            if True then re-calculate a new plan."""

        valr_sub_acc = self.SETTINGS.valr_DripDrip_acc_name
        acc_ID = self.VALR_EXCHANGE.get_account_ID(acc_label=valr_sub_acc)

        all_balances = self.VALR_EXCHANGE.get_balances(acc_ID=acc_ID, account_type="sub")
        ZAR_balances = self.VALR_EXCHANGE.parse_balances(balances=all_balances, coin="ZAR")
        enough_funds = False

        if float(ZAR_balances) >= float(500):
            enough_funds = True

        print("enough_funds:", enough_funds, ZAR_balances)

        return enough_funds, ZAR_balances




    def _set_CALCULATE_data(self, data):
        """ Sets the data for calculate_plan func. """

        # Reset
        self.set_dripData(key_name="plan", data=data)
        self.set_dripData(key_name="days_total", data=self.days)
        self.set_dripData(key_name="day_count", data=0)
        self.set_dripData(key_name="active", data=True)
        self.set_dripData(key_name="already_invested", data=False)
        self.set_dripData(key_name="last_invested_date", data="")






if __name__ == "__main__":

    DRIP = DripDrip()
    # DRIP.calculate_plan(5000)
    DRIP.total_value()


