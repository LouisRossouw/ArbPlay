from re import T
import utils
from time import sleep

from data import Data_log
from settings import Settings

from kucoin_exchange import Kucoin
from valr_exchange import Valr


class Algo_play():
    """ A class to store all the settings for algo play. """


    def __init__(self):
        """ Initialize algo settings. """

        self.kucoin = Kucoin()
        self.valr = Valr()
        self.SETTINGS = Settings()
        self.DATA_LOG = Data_log()

        self.TRADEPAIR_ALLOWED =  ["XRP", "SOL", "AVAX"]

        # Compatible trading pairs.
        self.VALR_COINPAIR = ["ETHZAR", "BTCZAR", "XRPZAR", "BNBZAR", "SOLZAR", "AVAXZAR", "SHIBZAR"]
        self.KUCOIN_COINPAIR = ["ETH-USDC", "BTC-USDC", "XRP-USDC", "BNB-USDC", "SOL-USDC", "AVAX-USDC", "SHIB-USDC"]




    def run(self):
        """ Main trading algo happens here."""

        self.valr_data = self.valr.return_coinPair_group(coinpair_group=self.VALR_COINPAIR)
        kucoin_data = self.kucoin.return_coinPair_group(coinpair_group=self.KUCOIN_COINPAIR)
        
        # Compare prices between 2 exchanges.
        return_analyse = self.compare(self.valr_data[0], kucoin_data)

        self.signal(return_analyse)




    def _check_USDC(self):
        """ PT of: execute_trade 1. : Check if there is enough USDT for trade execution. """

        # Get all Kucoin Accounts
        all_accounts = self.kucoin.client.get_accounts()

        # 1. check if enough USDC in account.
        USDT_account = self.kucoin.get_account(coin="USDT", 
                                               accounts=all_accounts, 
                                               account_type="trade")

        USDT_balance = USDT_account["balance"].split('.')[0]
        if USDT_account != None:

            if float(USDT_balance) >= 50:
                enough_usdc = True
            else:
                enough_usdc = False

        return enough_usdc, USDT_balance




    def _buy_coins(self, coin, coin_pairs, USDT_balance):
        """ PT of: execute_trade 2. : Buy order of specific coins. """

        self.kucoin.buy_coin(coin_pair=coin_pairs, amount_in_USDT=USDT_balance)

        # 2.2. while loop until funds reflect in the coins address,
        KUCOIN_Funds_ready = self.wait_for_funds_KUCOIN(coin)

        return KUCOIN_Funds_ready




    def _execute_withdraw(self, coin):
        """ PT of: execute_trade 2. : Execute Withdraw procedure. """

        try:
            accounts = self.kucoin.client.get_accounts()
            coin_account = self.kucoin.get_account(coin=coin, 
                                                   accounts=accounts, 
                                                   account_type="trade")["balance"]

            self.kucoin.inner_transfer(coin=coin, 
                                       from_account="trade", 
                                       to_account="main", 
                                       amount_coins=coin_account)
            sleep(2)
            valr_coin_info = self.valr.return_account_wallet_address(coin=coin, 
                                                                    subaccount_id="main", 
                                                                    account_type="main")

            # If there is no memo tag, then catch exception.
            try:
                valr_memo_TAG = valr_coin_info["paymentReference"]
            except EXCEPTION as e:
                valr_memo_TAG = ""
                
            valr_coin_address = valr_coin_info["address"]
            result = self.kucoin.withdrawal_to_address(coin=coin, 
                                                       amount_of_coin=coin_account, 
                                                       wallet_address=valr_coin_address, 
                                                       memo_tag=valr_memo_TAG)  # Transfer to valr exchange.

            self.DATA_LOG.set_kucoin_Coin(coin)
            self.DATA_LOG.set_kucoin_amount(coin_account)

            print("withdrawn ", result)
            is_withdrawn = True

        except Exception as e:

            print("Withdraw failed ", print(e))
            is_withdrawn = False

        return is_withdrawn




    def execute_trade_reverse(self, coin, percent_difference, percent_increase):
        """ Run the reverse - execution of the trade between the exchanges. VALR TO KUCOIN. """

        # 6. execute market sell order if XRP - usdc, if value == the same as bought price.
        # 7. wait for a new arbitrage oppertunity. - repeat

        enough_ZAR = False
        execute_valr_orders = self.SETTINGS.execute_order_valr

        print("\n*** Reverse Arbitrage oppertunity - ", coin, str(percent_difference) + "%")

        # # 1. check if enough ZAR in account.
        ZAR_balance = self.valr.Valr_get_balances(type="main")["ZAR"]["available"]
        if float(ZAR_balance) >= float(1000):
            enough_ZAR = True
            
        # # 2.1. BUY WITH ZAR, if no ZAR available, then pass
        if enough_ZAR == True:
            if execute_valr_orders == True:
                print("VALR - BUY ", coin, " R", ZAR_balance)
                self.valr.BUY_ZAR_to_coin(amount_in_coins=ZAR_balance, coin_pair=coin+"ZAR")

        enough_COIN = False
        while enough_COIN != True:
            COIN_balance = self.valr.Valr_get_balances(type="main")[coin]["available"]
            print("VALR - Checking coin Balance ", COIN_balance, coin)
            sleep(2)
            if float(COIN_balance) >= float(1):
                enough_COIN = True
                break
        
        if enough_COIN == True:
            print("VALR - WITHDRAW to Kucoin ", coin, COIN_balance)



        # if self.SETTINGS.execute_order == True:
        #     if enough_ZAR == True:

        #         # 2.2 Buy coin and return True if in account.
        #         VALR_Funds_ready = "self._buy_coins(coin, coin_pairs, USDT_balance)"

        #         # 2.3. execute transfer to local wallet.
        #         if VALR_Funds_ready == True:
        #             self.is_withdrawn = "self._execute_withdraw(coin)"

        # # 3. KUCOIN - check for funds, execute sell order when they have arived.
        # funds_arived_valr = "self._check_valr_funds(self.is_withdrawn, coin)"
        # if funds_arived_valr == True:
            
        #     print("self.execute_sell_coins_valr(coin)")





    def execute_trade(self, coin, percent_difference, percent_increase):
        """ Run the execution of the trade between the exchanges. KUCOIN TO VALR. """

        coin_pairs = coin + '-USDT'
        self.is_withdrawn = False

        # 1. check if enough USDC in account.
        enough_usdc = self._check_USDC()
        USDT_balance = enough_usdc[1]

        print("\n*** Arbitrage oppertunity - ", coin, str(percent_difference) + "%", " | R"+ str(percent_increase), " | enough USDT: " + str(enough_usdc[0]), " | USDT: : " + str(USDT_balance))

        # 2.1. BUY WITH USDC, if no USDC available, then pass
        if self.SETTINGS.execute_order == True:
            if enough_usdc[0] == True:

                self.DATA_LOG.set_kucoin_USDT(USDT_balance)

                # 2.2 Buy coin and return True if in account.
                KUCOIN_Funds_ready = self._buy_coins(coin, coin_pairs, USDT_balance)

                # 2.3. execute transfer to local wallet.
                if KUCOIN_Funds_ready == True:
                    self.is_withdrawn = self._execute_withdraw(coin)

        # 3. valr - check for funds, execute sell order when they have arived.
        funds_arived_valr = self._check_valr_funds(self.is_withdrawn, coin)
        if funds_arived_valr == True:
            if self.SETTINGS.execute_order_valr == True:
                self.execute_sell_coins_valr(coin)

                coin_quotes = self.kucoin.get_withdrawal_quotas(coin=coin)
                self.DATA_LOG.set_kucoin_coin_fee(coin_fee=coin_quotes["withdrawMinFee"])



    def _check_valr_funds(self, is_withdrawn, coin):
        """ After Kucoin has withdrawn, wait and check that it has arrived in Valr. """

        # 3. Check if crypto has arrived on local wallet.
        if is_withdrawn != False:
            VALR_Funds_readyself = self.wait_for_funds_VALR(coin)
        else:
            VALR_Funds_readyself = False

        # 4. If True - execute a sell market order on local exchange
        if VALR_Funds_readyself == True:
            print("Funds have arived on valr: ", coin)

        return VALR_Funds_readyself




    def execute_sell_coins_valr(self, coin):
        """ Execute a sell order on valr exchange after funs has arived in account from Kucoin."""

        print("Valr - Selling: ", coin)

        balances = self.valr.Valr_get_balances(type="main")
        coin_balance = balances[coin]["available"]

        self.valr.SELL_coin_to_ZAR(amount_in_coins=coin_balance, 
                                   coin_pair=coin + "ZAR")

        sleep(5)

        ZAR_funds = False
        while ZAR_funds != True:
            ZAR_balance = self.valr.Valr_get_balances(type="main")["ZAR"]["available"]
            print("checking ZAR funds ", ZAR_balance)
            sleep(3)
            if float(ZAR_balance) >= float(500):
                break

        # Set system to reverse arbitrage - we need to get the funds back to Kucoin at the cheapest cost.
        self.DATA_LOG.set_fund_position(position="reverse_arbitrage")
        self.DATA_LOG.set_valr_ZAR(ZAR_amount=ZAR_balance)




    def wait_for_funds_VALR(self, coins):
        """ waits in a while loop until funds arive in the coins account. - VALR """

        sleep(10)
        acc_name = self.SETTINGS.valr_arbitrage_acc_name
        ID = self.valr.get_account_ID(acc_label=acc_name)

        self.coin_account_value = False
        while self.coin_account_value != True:
            sleep(2)

            bal = self.valr.get_balances(acc_ID=ID, account_type="main")
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
            coin_account = self.kucoin.get_account(coin=coin, 
                                                   accounts=all_accounts, 
                                                   account_type="trade")

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

        # the value that will trigger as an oppertunity, 4% price increase would trigger an abritrage for example.
        percent_trigger = self.SETTINGS.percent_trigger
        reverse_percent_trigger = self.SETTINGS.reverse_percent_trigger 

        force_signal = self.SETTINGS.force_signal[0]
        force_coin = self.SETTINGS.force_signal[1]
        position = self.DATA_LOG.return_funds_position()

        # Force a signal execution to run tests.
        if force_signal == True:
            self.execute_trade(force_coin, " // ", " // ")

        else:
            for data in return_analyse:
                for allowed in self.TRADEPAIR_ALLOWED:
                    if allowed in data:

                        percent_difference = return_analyse[data][0]
                        growth_potential = return_analyse[data][1]            

                        if position == "arbitrage":

                            # if the arbitrage spread is greater than. then execute the trade from Kucoin to Valr.
                            if percent_difference >= percent_trigger:
                                self.execute_trade(allowed, percent_difference, growth_potential)

                        elif position == "reverse_arbitrage":

                            # if the reverse arbitrage spread is less than. then execute the trade from Valr to Kucoin.
                            if percent_difference <= reverse_percent_trigger:
                                self.execute_trade_reverse(allowed, percent_difference, growth_potential)




    def compare(self, exchange_local, exchange_international):
        """ Compares the price difference betweem local and international. """

        data = {}
        kucoin_fiat_prices = self.kucoin.get_fiat_price_for_coin(fiat="ZAR")

        print(self.DATA_LOG.return_funds_position())

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

    RUN = False
    SIGNAL = False
    ANALYSE = False
    COMPARE = False
    EXECUTE_TRADE = False
    PRINT_STATEMENT = False
    WAIT_FOR_FUNDS_KUCOIN = False
    WAIT_FOR_FUNDS_VALR = False
    EXECUTE_SELL_COINS_VALR = False
    EXECUTE_TRADE_REVERSE = True

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

    if EXECUTE_SELL_COINS_VALR == True:
        algo_play.execute_sell_coins_valr(coin="SOL")

    if EXECUTE_TRADE_REVERSE == True:
        algo_play.execute_trade_reverse(coin="XRP", percent_difference=1, percent_increase=1)
