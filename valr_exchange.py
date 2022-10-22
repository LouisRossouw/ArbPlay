import os
from settings import Settings

from valr_python import Client
from valr_python.exceptions import IncompleteOrderWarning



class Valr():
    """ A class for Valr. """

    def __init__(self):
        """ Initialize trading Valr. """

        self.SETTINGS = Settings()

        self.VALR_KEY = os.getenv('VALR_API_KEY')
        self.VALR_SECRET_KEY = os.getenv('VALR_API_KEY_SECRET')
        self.Valr_client = Client(api_key=self.VALR_KEY, api_secret=self.VALR_SECRET_KEY)






    def return_account_wallet_address(self, coin, subaccount_id, account_type):
        """ returns the wallet address for the specific coin, 
        if a subaccount ID is not given, it will use the default address. """

        if account_type == "sub":
            address = self.Valr_client.get_deposit_address(currency_code=coin, subaccount_id=subaccount_id)
        if account_type == "main":
            address = self.Valr_client.get_deposit_address(currency_code=coin)

        return address




    def return_coinPair_group(self, coinpair_group):
        """ returns a dict for inputed coinpair group, requires a list input. """

        market_data = self.Valr_client.get_market_summary()
        data = []

        for coin in coinpair_group:
            coinpair = self.return_coinPair_data(coin, market_data)
            data.append(coinpair)

        USDCZAR = self.return_coinPair_data("USDCZAR", market_data)

        return data, USDCZAR




    def return_coinPair_data(self, coinpair, market_data):
        """ Return the current bid and ask for a specific coin. """

        for i in market_data:
            symbol = i["currencyPair"]

            if symbol == coinpair:
                coin_data = i

        return coin_data




    def Valr_get_balances(self, type):
        """ gets my account wallets balances """

        if type == 'main':
            bal = self.Valr_client.get_balances()
        elif type != 'main':
            bal = self.Valr_client.get_balances(subaccount_id=type)

        data = {}

        for i in bal:
            currency = i['currency']
            available = i['available']
            reserved = i['reserved']
            total = i['total']
            data[currency] = {'available' : available, 'reserved' : reserved, 'total' : total}

        return data




    def get_account_ID(self, acc_label):
        """ Returns accounts ID. """

        acc_label = self.SETTINGS.valr_arbitrage_acc_name
        all_accounts = self.Valr_client.get_subaccounts()

        for acc in all_accounts:
            label = acc["label"]
            id = acc["id"]

            if acc_label == label:
                returned_label = id

        return returned_label




    def get_balances(self, acc_ID, account_type):
        """ Returns Balances for the specific account. """

        if account_type == "sub":
            balances = self.Valr_client.get_balances(subaccount_id=str(acc_ID))
        if account_type == "main":
            balances = self.Valr_client.get_balances()    

        return balances




    def parse_balances(self, balances, coin):
        """ Returns Balances for the specific account. """

        for currency in balances:
            currency_coin = currency["currency"]
            if currency_coin == coin:
                available = currency["available"]

        return available




    def SELL_coin_to_ZAR(self, amount_in_coins, coin_pair):
        """ Sell coin to Zar. """  

        self.Valr_client.post_market_order(
                            pair=str(coin_pair),
                            side='SELL',
                            base_amount= str(amount_in_coins)
                            )




    def BUY_ZAR_to_coin(self, amount_in_coins, coin_pair):
        """ Buy Zar to coin. """

        

        self.Valr_client.post_market_order(
                            pair=str(coin_pair),
                            side='BUY',
                            base_amount= str(amount_in_coins),
                            )




if __name__ == "__main__":

    valr_c = Valr()

    COINPAIR = "AVAXZAR"
    COINPAIR_GRP = ["XRPZAR", "ETHZAR", "BTCZAR"]

    acc_name = valr_c.SETTINGS.valr_arbitrage_acc_name

    GET_VALR_MARKET = False
    VALR_GET_BALANCES = False
    RETURN_COINPAIR_DATA = True
    RETURN_COINPAIR_GROUP = False
    GET_ACCOUNT_ID = False
    GET_BALANCES = False
    RETURN_ACCOUNT_WALLET_ADDRESS = False
    TEST = False

    if GET_VALR_MARKET == True:
        print(valr_c.get_valr_market())

    if VALR_GET_BALANCES == True:
        print(valr_c.Valr_get_balances(type="main"))

    if RETURN_COINPAIR_DATA == True:
        market_data = valr_c.Valr_client.get_market_summary()
        print(valr_c.return_coinPair_data(coinpair=COINPAIR, market_data=market_data))

    if RETURN_COINPAIR_GROUP == True:
        print(valr_c.return_coinPair_group(coinpair_group=COINPAIR_GRP))

    if GET_ACCOUNT_ID == True:
        print(valr_c.get_account_ID(acc_label=acc_name))

    if GET_BALANCES == True:
        ID = valr_c.get_account_ID(acc_label=acc_name)
        bal = valr_c.get_balances(acc_ID=ID, account_type="main")
        print(valr_c.parse_balances(balances=bal, coin="AVAX"))

    if RETURN_ACCOUNT_WALLET_ADDRESS == True:
        sub_ID = valr_c.get_account_ID(acc_label=acc_name)
        print(valr_c.return_account_wallet_address(coin="XRP", subaccount_id=sub_ID, account_type="main"))

    if TEST == True:
        valr_c.Valr_client.post_crypto_withdrawal()
        #prin9t(valr_c.Valr_client.get_whitelisted_address_book())
        #print(valr_c.Valr_client.get_crypto_withdrawal_status(currency_code="XRP"))
        #print(valr_c.Valr_client.post_fiat_withdrawal())

