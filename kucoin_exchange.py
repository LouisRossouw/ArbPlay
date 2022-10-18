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





    def get_withdrawal_quotas(self, coin):
        """ Retrieves the cost of transfer for the specific coin. (0.5 XRP) x Rands = value in Rands. """
        quote = self.client.get_withdrawal_quotas(currency=coin)
        return quote



    def get_deposit_address(self, coin):
        """ Retrieves the wallet address for a specific coin. (might need to create one first)"""
        address = self.client.get_deposit_address(currency=coin)
        return address



    def get_fiat_price_for_coin(self, fiat):
        """ Return the value of the coin in any fiat, perfect to find ZAR value on Kucoin. """
        data = self.client.get_fiat_prices(base=fiat)
        return data




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




    def buy_coin(self, coin_pair, amount_in_USDT):
        """ Performs a market buy function. """

        allow_place_order = self.SETTINGS.execute_order

        if allow_place_order == True:
                                        # 'AFK-USDT'
            self.client.create_market_order(coin_pair, "buy", funds=amount_in_USDT)
        elif allow_place_order == False:
            print("** placing orders are dissabled in the Settings.py file. ** ")




    def sell_coin(self, coin_pair, amount_in_coins):
        """ Performs a market buy function. """

        allow_place_order = self.SETTINGS.execute_order

        if allow_place_order == True:
                                        # 'AFK-USDT'
            self.client.create_market_order(coin_pair, "sell", size=amount_in_coins)
        elif allow_place_order == False:
            print("** placing orders are dissabled in the Settings.py file. ** ")




    def withdrawal_to_address(self, coin, amount_of_coin, wallet_address):
        """ Withdraws currency and transfers it to the new address. """

        allow_withdraws = self.SETTINGS.execute_withdrawels

        if allow_withdraws == True:
            self.client.create_withdrawal(currency=coin, amount=amount_of_coin, address=wallet_address, remark="Arbitrage_to_Valr",)
        else:
            print("** Withdrawels are dissabled in the Settings.py file. ** ")



if __name__ == "__main__":

    kucoin_class = Kucoin()

    COINPAIR = "XRP-USDC"
    COINPAIR_GRP = ["XRP-USDC", "ETH-USDC", "BTC-USDC"]

    RETURN_COINPAIR_DATA = False
    RETURN_COINPAIR_GROUP = False
    RETURN_ACCOUNT = False
    GET_ACCOUNT = False
    GET_FIAT_PRICE_FOR_COIN = False
    WITHDRAWEL_TO_ADDRESS = True
    SELL_COIN = False
    BUY_COIN = False


    if RETURN_COINPAIR_DATA == True:
        market_data = kucoin_class.client.get_ticker()["ticker"]
        print(kucoin_class.return_coinPair_data(coinpair=COINPAIR, market_data=market_data))

    if RETURN_COINPAIR_GROUP == True:
        print(kucoin_class.return_coinPair_group(coinpair_group=COINPAIR_GRP))

    if RETURN_ACCOUNT == True:
        print(kucoin_class.return_account(coin="AFK"))

    if GET_ACCOUNT == True:
        # IMPORTANT - it is locked to a fixed IP address on kucoin, - need to make IP adress fixed.
        accounts = kucoin_class.client.get_accounts()
        print(kucoin_class.get_account(coin="USDT", accounts=accounts))

    if GET_FIAT_PRICE_FOR_COIN == True:
        print(kucoin_class.get_fiat_price_for_coin(fiat="ZAR")["AFK"])

    if WITHDRAWEL_TO_ADDRESS == True:
        kucoin_class.withdrawal_to_address(coin="SHIB", amount_of_coin=5100, wallet_address="123456")

    if SELL_COIN == True:
        kucoin_class.sell_coin(coin_pair="AFK-USDT", amount_in_USDT="10")

    if BUY_COIN == True:
        kucoin_class.buy_coin(coin_pair="SHIB-USDT", amount_in_USDT=10)
