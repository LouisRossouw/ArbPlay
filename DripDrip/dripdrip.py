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
        self.sampleList = ["XRP", "BTC", "ADA", "SOL"]
        self.weights = [70, 50, 20, 10]

        self.data = {
                        "XRP": 70,
                        "BTC": 50,
                        "ADA": 20,
                        "SOL": 10,
                    }



    def set_plan(self):
        """ Sets the drip plan into the data.json. """
        pass




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

        randomList = random.choices(coins, weights=coin_values, k=self.amount_capital)
            
        data = {}
        for i in coins:

            coin_amount = randomList.count(i)
            data[i] = coin_amount / self.days

        print(data)






    def check_newDay(self):
        """ Check if it is a new day, if True, execute trade. """
        print("checkcheck")
        return True



    def run(self):
        """ Runs drip. """

        # Check if its a new day, if True, execute trade.
        is_NewDay = self.check_newDay()

        if is_NewDay == True:
            
            # Collect data
            drip_data = utils.read_json(f"{os.path.dirname(__file__)}/drip_data.json")

            # If time is now, then invest
            if drip_data["time"] == self.invest_time:
                pass


                if drip_data["already_invested"] != True:
                    pass






if __name__ == "__main__":

    DRIP = DripDrip()
    DRIP.calculate_plan()   



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