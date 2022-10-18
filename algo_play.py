from time import sleep
import utils
from settings import Settings

from kucoin_exchange import Kucoin
from valr_exchange import Valr

from forex_python.converter import CurrencyRates

class Algo_play():
    """ A class to store all the settings for algo play. """


    def __init__(self):
        """ Initialize algo settings. """

        self.kucoin = Kucoin()
        self.valr = Valr()
        self.SETTINGS = Settings()

        self.TRADEPAIR_ALLOWED =  ["XRP", "BNB", "SOL", "AVAX", "SHIB"]

        # Compatible trading pairs.
        self.VALR_COINPAIR = ["ETHZAR", "BTCZAR", "XRPZAR", "BNBZAR", "SOLZAR", "AVAXZAR", "SHIBZAR"]
        self.KUCOIN_COINPAIR = ["ETH-USDC", "BTC-USDC", "XRP-USDC", "BNB-USDC", "SOL-USDC", "AVAX-USDC", "SHIB-USDC"]






    def run(self):
        """ Main trading algo happens here."""

        # cr = CurrencyRates()
        # self.ZAR = cr.get_rates("USD")["ZAR"]
        self.valr_data = self.valr.return_coinPair_group(coinpair_group=self.VALR_COINPAIR)
        kucoin_data = self.kucoin.return_coinPair_group(coinpair_group=self.KUCOIN_COINPAIR)
        
        # Compare prices between 2 exchanges.
        return_analyse = self.compare(self.valr_data[0], kucoin_data)

        self.signal(return_analyse)




    def execute_trade(self, coin, percent_difference, percent_increase):
        """ Run the execution of the trade between the exchanges. """

        enough_usdc = None
        self.coin_account_value = None

        # Get all Kucoin Accounts
        all_accounts = self.kucoin.client.get_accounts()

        # 0. check if coin has already been bought.
        coin_account = self.kucoin.get_account(coin=coin, accounts=all_accounts)
        if coin_account != None:
            if float(coin_account["balance"]) >= 10000000: # NEED TO FIX THIS, IT CURRENTLY IS BASED ON BASE COIN CURRENCY AND NOT USDT
                print("enough coins")
                self.coin_account_value = True

        # 1. check if enough USDC in account.
        USDT_account = self.kucoin.get_account(coin="USDT", accounts=all_accounts)
        USDT_balance = USDT_account["balance"]
        if USDT_account != None:
            if float(USDT_balance) >= 40:
                enough_usdc = True

        coin_pairs = coin + '-USDT'
        print("\n*** Arbitrage oppertunity - ", coin, str(percent_difference) + "%", " | R"+ str(percent_increase), " | enough USDC: " + str(bool(enough_usdc)), " | Existing coins: " + str(bool(self.coin_account_value)))


        # 2. execute a buy market order on international exchange,
        if self.coin_account_value != None:
            # 2.1. execute transfer to local wallet.
            self.kucoin.transfer_coin_to_address(coin=coin, amount=10, address="1234")


        elif self.coin_account_value == None:
            # 2.1. BUY WITH USDC, if no USDC available, the pass
            if enough_usdc == True:
                self.kucoin.buy_coin(coin_pair=coin_pairs, amount_in_USDT=float(USDT_balance) - 1)

                # 2.2. while loop until funds reflect in the coins address,
                KUCOIN_Funds_ready = self.wait_for_funds_KUCOIN(coin)

                # 2.3. execute transfer to local wallet.
                if KUCOIN_Funds_ready == True:
                    self.kucoin.transfer_coin_to_address(coin=coin, amount=10, address="1234")



        # 3. Check if crypto has arrived on local wallet.
        if self.coin_account_value != None:
            VALR_Funds_readyself = self.wait_for_funds_VALR(coin)
        else:
            VALR_Funds_readyself = False

        # 4. If True - execute a sell market order on local exchange
        if VALR_Funds_readyself == True:
            pass


        # 5. Buy XRP, transfer XRP to international wallet.

        # 6. execute market sell order if XRP - usdc, if value == the same as bought price.

        # 7. wait for a new arbitrage oppertunity. - repeat



    def wait_for_funds_VALR(self, coins):
        """ waits in a while loop until funds arive in the coins account. - VALR """

        acc_name = self.SETTINGS.valr_arbitrage_acc_name
        ID = self.valr.get_account_ID(acc_label=acc_name)

        self.coin_account_value = False
        while self.coin_account_value != True:
            sleep(2)

            bal = self.valr.get_balances(acc_ID=ID)
            local_coin_wallet = self.valr.parse_balances(balances=bal, coin=coins)

            print("VALR - Checking Funds. - ", local_coin_wallet, coins)

            if float(local_coin_wallet) >= float(50):
                self.coin_account_value = True
                if self.coin_account_value == True:
                    print("VALR - Funds True", coins)
                    break

        return True




    def wait_for_funds_KUCOIN(self, coin):
        """ waits in a while loop until funds arive in the coins account. - KUCOIN """

        self.coin_account_value = False
        while self.coin_account_value != True:
            sleep(2)
            # Get all Kucoin Accounts
            all_accounts = self.kucoin.client.get_accounts()
            coin_account = self.kucoin.get_account(coin=coin, accounts=all_accounts)
            print("kucoin - Checking Funds. - ", coin_account, coin)
            if coin_account != None:
                if float(coin_account["balance"]) >= 50:
                    self.coin_account_value = True
                    if self.coin_account_value == True:
                        print("KUCOIN - Funds True", coin)
                        break

        return True



    def signal(self, return_analyse):
        """ Runs through the analyse data and if data is true, execute a True signal. """

        percent_trigger = self.SETTINGS.percent_trigger # the value that will trigger as an oppertunity, 4% price increase would trigger an abritrage for example.

        for data in return_analyse:
            for allowed in self.TRADEPAIR_ALLOWED:
                if allowed in data:

                    percent_difference = return_analyse[data][0]
                    growth_potential = return_analyse[data][1]            

                    # if the arbitrage spread is greater than. then execute the trade.
                    if percent_difference >= percent_trigger:
                        self.execute_trade(allowed, percent_difference, growth_potential)




    def compare(self, exchange_local, exchange_international):
        """ Compares the price difference betweem local and international. """

        data = {}
        kucoin_fiat_prices = self.kucoin.get_fiat_price_for_coin(fiat="ZAR")

        # i can buy at kucoin int_ask and sell at valr loc_bid
        for i in range(len(exchange_local)):

            loc_currencyPair = exchange_local[i]["currencyPair"]
            loc_ask = exchange_local[i]["askPrice"]
            loc_bid = exchange_local[i]["bidPrice"]

            int_currencyPair = exchange_international[i]["symbol"]
            int_ask_usdc = exchange_international[i]["sell"]
            int_bid_usdc = exchange_international[i]["buy"]

            coin = int_currencyPair.split("-")[0]
            int_coin_zar = kucoin_fiat_prices[coin]

            return_analyse = self.analyse(loc_bid, int_coin_zar, 
                        loc_currencyPair, int_currencyPair)

            data[loc_currencyPair] = return_analyse

        return data




    def analyse(self, loc_bid, int_coin_zar, loc_currencyPair, int_currencyPair):
        """ Check the spread if its large enough to let an execution buy and sell. """

        percent_difference = round(utils.get_percentage_difference(loc_bid, int_coin_zar), 2)
        percent_increase = round(utils.percent_increase(percent_difference, self.SETTINGS.play_money), 3)

        self.print_statement(loc_bid, int_coin_zar, loc_currencyPair, percent_difference, percent_increase)

        return percent_difference, percent_increase





    def print_statement(self, loc_bid, int_coin_zar, loc_currencyPair, percent_difference, percent_increase):
        """ Prints out. """

        if self.SETTINGS.print_statements == True:
            print(loc_currencyPair, " |  R "+str(percent_increase), " | "+str(percent_difference) + "%", " | Valr price R"+ str(loc_bid), " | Kucoin price R"+str(round(float(int_coin_zar), 2)))
            if percent_difference >= 3:
                print(loc_currencyPair, " |  R "+str(percent_increase), " | "+str(percent_difference) + "%", "<<< **************** ")




if __name__ == "__main__":

    algo_play = Algo_play()

    RUN = True
    SIGNAL = False
    ANALYSE = False
    COMPARE = False
    EXECUTE_TRADE = False
    PRINT_STATEMENT = False
    WAIT_FOR_FUNDS_KUCOIN = False
    WAIT_FOR_FUNDS_VALR = False

    TRADEPAIR_ALLOWED =  ["ETH", "BTC", "XRPZ", "BNB", "SOL", "AVAX", "SHIB"]
    VALR_COINPAIR = ["ETHZAR", "BTCZAR", "XRPZAR", "BNBZAR", "SOLZAR", "AVAXZAR", "SHIBZAR"]
    KUCOIN_COINPAIR = ["ETH-USDC", "BTC-USDC", "XRP-USDC", "BNB-USDC", "SOL-USDC", "AVAX-USDC", "SHIB-USDC"]

    if RUN == True:
        algo_play.run()

    if EXECUTE_TRADE == True:
        algo_play.execute_trade(coin="XRP")

    if WAIT_FOR_FUNDS_KUCOIN == True:
        print(algo_play.wait_for_funds_KUCOIN(coin="XRP"))

    if PRINT_STATEMENT == True:
        algo_play.print_statement(18, 17, "XRPZAR", 5, 6)

    if ANALYSE == True:
        print(algo_play.analyse(19, 18, "XRPZAR", "XRP-USDC"))

    if SIGNAL == True:
        return_analyse = algo_play.compare(algo_play.valr_data[0], algo_play.kucoin_data)
        algo_play.signal(algo_play.valr_data[0], algo_play.kucoin_data)

    if COMPARE == True:
        valr_data = algo_play.valr.return_coinPair_group(coinpair_group=VALR_COINPAIR)
        kucoin_data = algo_play.kucoin.return_coinPair_group(coinpair_group=KUCOIN_COINPAIR)
        algo_play.compare(algo_play.valr_data[0], algo_play.kucoin_data)

    if WAIT_FOR_FUNDS_VALR == True:
        print(algo_play.wait_for_funds_VALR(coins="XRP"))