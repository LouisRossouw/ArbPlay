import os
import utils as utils
from settings import Settings


class Data_log():
    """ A class for data movement. """

    def __init__(self):
        """ Initialize data settings. """

        self.SETTINGS = Settings()

        self.data_path = self.return_arbitrage_trade()
        self.data_file = utils.read_json(self.data_path) 



    def return_data(self, key_name):

        data = utils.read_json(self.data_path)[key_name]
        return data



    def return_arbitrage_trade(self):
        """ returns the path to the arbitrage json file. """

        this_file = os.path.dirname(__file__)
        data_file = f"{this_file}/data/arbitrage.json"

        if os.path.exists(data_file) != True:
            data = {}
            utils.write_to_json(data_file, data)

        return data_file




    def return_funds_position(self):
        """ Returns the funds position. """

        position = utils.read_json(self.data_path)["position"]
        return position



    def return_valr_coin_askPrice(self):
        """ Returns the funds position. """

        valr_coin_askPrice = utils.read_json(self.data_path)["valr_coin_askPrice"]
        return valr_coin_askPrice



    def set_kucoin_USDT(self, USDT):
        """ Sets the current USDT balance before execution. """

        self.data_file["Kucoin_USDT"] = USDT
        utils.write_to_json(self.data_path, self.data_file)  



    def set_kucoin_coin_fee(self, coin_fee):
        """ Sets the coins transfer fee for withdrawels. """

        self.data_file["Kucoin_coin_fee"] = coin_fee
        utils.write_to_json(self.data_path, self.data_file)  




    def set_kucoin_Coin(self, coin):
        """ Sets the current USDT balance before execution. """

        self.data_file["Kucoin_coin"] = coin
        utils.write_to_json(self.data_path, self.data_file)  




    def set_kucoin_amount(self, amount_coins):
        """ Sets the current USDT balance before execution. """

        self.data_file["Kucoin_amount"] = amount_coins
        utils.write_to_json(self.data_path, self.data_file)  




    def set_fund_position(self, position):
        """ sets the position of the funds. """

        self.data_file["position"] = position
        utils.write_to_json(self.data_path, self.data_file)



    def set_valr_ZAR(self, ZAR_amount):
        """ sets the amount of ZAR deposited into the valr zar account from sale. """

        self.data_file["ZAR_funds"] = ZAR_amount
        utils.write_to_json(self.data_path, self.data_file)


    def set_valr_coin_askPrice(self, coin_price_ZAR):
        """ Sets the purchased value of the coin in ZAR. """

        self.data_file["valr_coin_askPrice"] = coin_price_ZAR
        utils.write_to_json(self.data_path, self.data_file)


    def set_valr_coin_amount(self, coin_amount):
        """ Sets the current USDT balance before execution. """

        self.data_file["valr_coin_amount"] = coin_amount
        utils.write_to_json(self.data_path, self.data_file)  



if __name__ == "__main__":

    data_log = Data_log()
