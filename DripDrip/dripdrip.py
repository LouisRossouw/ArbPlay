import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import toolUtils.utils as utils
import Exchanges.valr_exchange as VALR




class DripDrip():
    """ A class for the drip system. """

    def __init__(self):
        """ Initialize drip. """

        VALR_EXCHANGE = VALR.Valr()

        self.days = 10
        self.amount_capital = 10000
        self.invest_time = 8 # first 2 digits of a digital watch.
        self.drip_data_path = f"{os.path.dirname(__file__)}/drip_data.json"

        self.data = {
                        "XRP": 70,
                        "BTC": 50,
                        "ADA": 20,
                        "SOL": 10,
                    }




    def get_dripData(self, key_name):
        """ Generic get data from drip_data.json. """   

        drip_data = utils.read_json(self.drip_data_path)
        return drip_data[key_name]




    def set_dripData(self, key_name, data):
        """ Generic set data to drip_data.json. """
        
        drip_data = utils.read_json(self.drip_data_path)
        drip_data[key_name] = data
        utils.write_to_json(self.drip_data_path, drip_data)




    def calculate_plan(self):
        """ calculates the amount it must invest for each coin over the amount of days, 
            and sets it in the data. 
        """
        
        my_data = self.data

        coins = []
        coin_values = []

        for data in my_data:
            value = my_data[data]

            coins.append(data)
            coin_values.append(value)

        randomList = random.choices(coins, 
                                    weights=coin_values, 
                                    k=self.amount_capital)
            
        data = {}
        for i in coins:

            coin_amount = randomList.count(i)
            data[i] = coin_amount / self.days

        # Reset
        self.set_dripData(key_name="plan", data=data)
        self.set_dripData(key_name="days_total", data=self.days)
        self.set_dripData(key_name="day_count", data=0)
        self.set_dripData(key_name="active", data=True)
        self.set_dripData(key_name="already_invested", data=False)
        self.set_dripData(key_name="last_invested_date", data="")




    def invested_today(self):
        """ Check if it is a new day, if True, execute trade. """

        # compare the last investment date with the date now.
        invested_date = self.get_dripData(key_name="last_invested_date")
        todays_date = utils.get_dates()[0]

        if todays_date == invested_date:
            Invested_today = True
        else:
            Invested_today = False

        return Invested_today




    def buy_coins(self, drip_data):
        """ Execute multiple buys for coin in coin list and its amount. """

        plan = drip_data["plan"]

        for coin in plan:
            amount = plan[coin]
        
            print("Buy:", coin, amount)


            

    def run(self):
        """ Runs drip. """

        # Check if its a new day, if True, execute trade.
        invested_today = self.invested_today()
    
        if invested_today == False:

            active = self.get_dripData(key_name="active") 

            # if have not reached total days investing, then buy.
            if active != False:

                # Collect data
                drip_data = utils.read_json(self.drip_data_path)
                time_now = utils.get_dates()[1].split(":")[0] # get first hour only
                print(time_now)
                # If time is now, then invest
                if int(time_now) == self.invest_time:
                    print("time is golden")

                    if drip_data["already_invested"] != True:
                        print("have not invested - lets invest now!")

                        self.buy_coins(drip_data)

                        day_count = int(self.get_dripData(key_name="day_count"))

                        self.set_dripData(key_name="already_invested", data=True)
                        self.set_dripData(key_name="last_invested_date", data=utils.get_dates()[0])
                        self.set_dripData(key_name="day_count", data=day_count + 1)

                        total_days = self.get_dripData(key_name="days_total")

                        if int(day_count + 1) == int(total_days):
                            print("Done")
                            self.set_dripData(key_name="active", data=False)      
            else:
                # Else if have reached goal
                # then check, once a day, if the zar balance is  >= R500
                # if True, run the re-calculate function to set a new plan in place.
                print("Not active - deposit ZAR to activate bot.")





if __name__ == "__main__":

    DRIP = DripDrip()
    DRIP.run()   



    # randomList = random.choices(self.sampleList, weights=self.weights, k=self.amount_capital)
    
    # xrp_count = randomList.count("XRP")
    # btc_count = randomList.count("BTC")
    # ada_count = randomList.count("ADA")
    # sol_count = randomList.count("SOL")

    # days_amount = xrp_count / self.days, btc_count / self.days, ada_count / self.days, sol_count / self.days

    # xrp = days_amount[0]
    # btc = days_amount[1]
    # ada = days_amount[2]
    # sol = days_amount[3]

    # x = 0
    # b = 0
    # a = 0
    # s = 0

    # print("Run --", days_amount, "\n")

    # for i in range(1, self.days + 1):
        
    #     x += xrp
    #     b += btc
    #     a += ada
    #     s += sol

    #     print("Day:",i , round(x,2), round(b,2), round(a,2), round(s,2))


    # print("\nTotal -----", x, b, a, s)
    # print("=", x + b + a + s)