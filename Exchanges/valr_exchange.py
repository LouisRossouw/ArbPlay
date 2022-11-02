import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valr_python import Client
from valr_python.exceptions import IncompleteOrderWarning

import BotFido.BotNotifications as BotNot

import toolUtils.logger as LOG


class Valr():
    """ A class for Valr. """

    def __init__(self):
        """ Initialize trading Valr. """

        self.LOGLOG = LOG.LogLog().ExchangeLog()
        self.BOTNOT = BotNot.BotNotification()

        self.VALR_KEY = os.getenv('VALR_API_KEY')
        self.VALR_SECRET_KEY = os.getenv('VALR_API_KEY_SECRET')
        self.Valr_client = Client(api_key=self.VALR_KEY, api_secret=self.VALR_SECRET_KEY)




    def log_errors(self, e, log_error_1, log_error_2):
        """ logs errors and sends admin notification. """

        # Logs
        self.LOGLOG.error(e)

        # Telegram Admin notification.
        self.BOTNOT.send_ADMIN_notification(text=log_error_1)
        self.BOTNOT.send_ADMIN_notification(text=log_error_2 + str(e))




    def return_account_wallet_address(self, coin, subaccount_id, account_type):
        """ returns the wallet address for the specific coin, 
            if a subaccount ID is not given, it will use the default address. """

        log_success = f"VALR return_account_wallet_address: {str(coin)} | account_type:{str(account_type)}"
        log_error_1 = f"⛔️ VALR: ATTEMPTED return_account_wallet_address: \n\n{str(coin)}\naccount_type: {str(account_type)}"
        log_error_2 = f"⛔️ Error: return_account_wallet_address: "
        self.LOGLOG.info(log_success)

        try:
            if account_type == "sub":
                address = self.Valr_client.get_deposit_address(currency_code=coin, 
                                                            subaccount_id=subaccount_id)
            if account_type == "main":
                address = self.Valr_client.get_deposit_address(currency_code=coin)
        except Exception as e:
            address = False
            self.log_errors(e, log_error_1, log_error_2)

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

        log_success = f"VALR SELL_coin_to_ZAR: {str(coin_pair)} | amount_in_coins:{str(amount_in_coins)}"
        log_error_1 = f"⛔️ VALR: ATTEMPTED SELL_coin_to_ZAR: \n\n{str(coin_pair)}\namount_in_coins: {str(amount_in_coins)}"
        log_error_2 = f"⛔️ Error: SELL_coin_to_ZAR: "

        self.LOGLOG.info(log_success)

        try:
            self.Valr_client.post_market_order(
                                pair=str(coin_pair),
                                side='SELL',
                                base_amount= str(amount_in_coins)
                                )
        except Exception as e:
            self.log_errors(e, log_error_1, log_error_2)




    def BUY_ZAR_to_coin(self, amount_in_coins, coin_pair):
        """ Buy Zar to coin. """

        log_success = f"VALR BUY_ZAR_to_coin: {str(coin_pair)} | amount_in_coins:{str(amount_in_coins)}"
        log_error_1 = f"⛔️ VALR: ATTEMPTED BUY_ZAR_to_coin: \n\n{str(coin_pair)}\namount_in_coins: {str(amount_in_coins)}"
        log_error_2 = f"⛔️ Error: BUY_ZAR_to_coin: "

        self.LOGLOG.info(log_success)

        try:
            self.Valr_client.post_market_order(
                                pair=str(coin_pair),
                                side='BUY',
                                base_amount= str(amount_in_coins),
                                )
        except Exception as e:
            self.log_errors(e, log_error_1, log_error_2)




    def subAcc_BUY_ZAR_to_coin(self, amount_in_coins, coin_pair, sub_ID):
        """ Buy Zar to coin. """

        log_success = f"VALR subAcc_BUY_ZAR_to_coin: {str(coin_pair)} | amount_in_coins:{str(amount_in_coins)}"
        log_error_1 = f"⛔️ VALR: ATTEMPTED subAcc_BUY_ZAR_to_coin: \n\n{str(coin_pair)}\namount_in_coins: {str(amount_in_coins)}\nsub_id: {str(sub_ID)}"
        log_error_2 = f"⛔️ Error: subAcc_BUY_ZAR_to_coin: "

        self.LOGLOG.info(log_success)

        try:
            self.Valr_client.post_market_order(
                                pair=str(coin_pair),
                                side='BUY',
                                base_amount= str(amount_in_coins),
                                subaccount_id= sub_ID
                                )
        except Exception as e:
            self.log_errors(e, log_error_1, log_error_2)





if __name__ == "__main__":

    valr_c = Valr()

    COINPAIR = "USDCZAR"
    COINPAIR_GRP = ["XRPZAR", "ETHZAR", "BTCZAR"]

    acc_name = "test"

    GET_VALR_MARKET = False
    VALR_GET_BALANCES = False
    RETURN_COINPAIR_DATA = False
    RETURN_COINPAIR_GROUP = False
    GET_ACCOUNT_ID = False
    GET_BALANCES = False
    RETURN_ACCOUNT_WALLET_ADDRESS = True
    TEST = False

    if GET_VALR_MARKET == True:
        print(valr_c.get_valr_market())

    if VALR_GET_BALANCES == True:
        print(valr_c.Valr_get_balances(type="main"))

    if RETURN_COINPAIR_DATA == True:
        market_data = valr_c.Valr_client.get_market_summary()
        print(valr_c.return_coinPair_data(coinpair=COINPAIR, 
                                          market_data=market_data))

    if RETURN_COINPAIR_GROUP == True:
        print(valr_c.return_coinPair_group(coinpair_group=COINPAIR_GRP))

    if GET_ACCOUNT_ID == True:
        print(valr_c.get_account_ID(acc_label=acc_name))

    if GET_BALANCES == True:
        ID = valr_c.get_account_ID(acc_label=acc_name)
        bal = valr_c.get_balances(acc_ID=ID, account_type="main")
        print(valr_c.parse_balances(balances=bal, coin="AVAX"))

    if RETURN_ACCOUNT_WALLET_ADDRESS == True:
        # sub_ID = valr_c.get_account_ID(acc_label=acc_name)
        print(valr_c.return_account_wallet_address(coin="AVAX", 
                                                   subaccount_id="main", 
                                                   account_type="main"))

    if TEST == True:
        valr_c.Valr_client.post_crypto_withdrawal()
        #prin9t(valr_c.Valr_client.get_whitelisted_address_book())
        #print(valr_c.Valr_client.get_crypto_withdrawal_status(currency_code="XRP"))
        #print(valr_c.Valr_client.post_fiat_withdrawal())

