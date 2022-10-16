from locale import currency
import os

from kucoin.client import Client
from settings import Settings

class Kucoin():
    """ A class for Kucoin. """

    def __init__(self):
        """ Initialize trading Kucoin. """

        self.SETTINGS = Settings()

        api_key = os.getenv('KUCOIN_API_KEY')
        api_secret = os.getenv('KUCOIN_API_KEY_SECRET')
        api_passphrase = os.getenv('KUCOIN_PHASSPHRASE')

        self.client = Client(api_key, api_secret, api_passphrase)
        # or connect to Sandbox
        # client = Client(api_key, api_secret, api_passphrase, sandbox=True)




    def return_coinPair_group(self, coinpair_group):
        """ returns a dict for inputed coinpair group, requires a list input. """

        market_data = self.client.get_ticker()["ticker"]
        data = []

        for coin in coinpair_group:
            coinpair = self.return_coinPair_data(coin, market_data)
            data.append(coinpair)

        return data




    def return_coinPair_data(self, coinpair, market_data):
        """ Return the current bid and ask for a specific coin. """

        for i in market_data:
            symbol = i["symbol"]

            if symbol == coinpair:
                coin_data = i

        return coin_data




    def check_USDC_amount(self):
        """ Returns the amount of USDC in account. """


        pass
    



    def return_account(self, coin):
        """ Incase i want to change this to a group later on. """

        accounts = self.client.get_accounts()
        data = self.get_account(coin=coin, accounts=accounts)

        return data




    def get_account(self, coin, accounts):
        """ Returns existing accounts on Kucoin.
        # IMPORTANT - it is locked to a fixed IP address on kucoin, - need to make IP adress fixed.
        """

        data = None

        for account in range(len(accounts)):
            currency_coin = (accounts[account]["currency"])
            type = (accounts[account]["type"])
            balance = (accounts[account]["balance"])

            if coin == currency_coin:
                if type == "trade":
                    data = {"currency_coin":currency_coin, "type":type, "balance":balance}
            else:
                pass

        return data



    def buy_coin(self, coin, amount):
        """ Performs a market buy function. """
        pass



    def transfer_coin_to_address(self, coin, amount, address):
        """ Performs a market buy function. """
        pass



if __name__ == "__main__":

    kucoin_class = Kucoin()

    COINPAIR = "XRP-USDC"
    COINPAIR_GRP = ["XRP-USDC", "ETH-USDC", "BTC-USDC"]

    RETURN_COINPAIR_DATA = False
    RETURN_COINPAIR_GROUP = False
    RETURN_ACCOUNT = False
    GET_ACCOUNT = True



    if RETURN_COINPAIR_DATA == True:
        market_data = kucoin_class.client.get_ticker()["ticker"]
        print(kucoin_class.return_coinPair_data(coinpair=COINPAIR, market_data=market_data))

    if RETURN_COINPAIR_GROUP == True:
        print(kucoin_class.return_coinPair_group(coinpair_group=COINPAIR_GRP))

    if RETURN_ACCOUNT == True:
        print(kucoin_class.return_account(coin="USDC"))

    if GET_ACCOUNT == True:
        # IMPORTANT - it is locked to a fixed IP address on kucoin, - need to make IP adress fixed.
        accounts = kucoin_class.client.get_accounts()
        print(kucoin_class.get_account(coin="XRP", accounts=accounts))

