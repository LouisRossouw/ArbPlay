import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep

from data import Data_log
from Settings import Settings

from Exchanges.kucoin_exchange import Kucoin
from Exchanges.valr_exchange import Valr

import toolUtils.logger as LOG


class Algo_arbitrage():
    """ A class to store all the settings for algo play. """

    def __init__(self):
        """ Initialize algo settings. """

        self.kucoin = Kucoin()
        self.valr = Valr()
        self.SETTINGS = Settings()
        self.DATA_LOG = Data_log()




    def execute_trade(self, coin, percent_difference, percent_increase):
        """ Run the execution of the trade between the exchanges. KUCOIN TO VALR. """

        self.is_withdrawn = False

        # 1. check if enough USDC in account. # Returns list, bool and amount
        enough_usdc = self._check_USDC() 

        self._PRINT_arbitrage(coin, 
                              percent_difference, 
                              percent_increase, 
                              enough_usdc, enough_usdc[1])

        # 2.1. BUY WITH USDC, if no USDC available, then pass
        if self.SETTINGS.execute_order == True:
            if enough_usdc[0] == True:

                self.DATA_LOG.set_data(key_name="Kucoin_USDT", data=enough_usdc[1])

                # 2.2 Buy coin and return True if in account.
                KUCOIN_Funds_ready = self._buy_coins(coin, 
                                                     coin + '-USDT', 
                                                     enough_usdc[1])

                # 2.3. execute transfer to local wallet.
                if KUCOIN_Funds_ready == True:
                    self.is_withdrawn = self._execute_withdraw(coin)

        # 3. valr - check for funds, execute sell order when they have arived.
        funds_arived_valr = self._check_valr_funds(self.is_withdrawn, coin)
        
        if funds_arived_valr == True:
            if self.SETTINGS.execute_order_valr == True:
                self._execute_sell_coins_valr(coin)

                coin_quotes = self.kucoin.get_withdrawal_quotas(coin=coin)
                self.DATA_LOG.set_data(key_name="Kucoin_coin_fee", 
                                       data=coin_quotes["withdrawMinFee"])




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
        """ Buy order of specific coins. and while loop until coins arive."""

        LOG.ArbitrageLog.info(f"Kucoin - Buying coins: {str(coin)}|pairs:{str(coin_pairs)}|USDT:{str(USDT_balance)}")
        self.kucoin.buy_coin(coin_pair=coin_pairs, amount_in_USDT=USDT_balance)
        KUCOIN_Funds_ready = self._wait_for_funds_KUCOIN(coin, acc_type="trade")
        
        return KUCOIN_Funds_ready




    def _execute_withdraw(self, coin):
        """ PT of: execute_trade 2. : Execute Withdraw procedure. """

        LOG.ArbitrageLog.info(f"Kucoin - Attempting Withdraw: {str(coin)}")

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
            except Exception as e:
                valr_memo_TAG = ""
                
            valr_coin_address = valr_coin_info["address"]
            result = self.kucoin.withdrawal_to_address(
                                                       coin=coin, 
                                                       amount_of_coin=coin_account, 
                                                       wallet_address=valr_coin_address, 
                                                       memo_tag=valr_memo_TAG) # Transfer to valr exchange.

            self.DATA_LOG.set_data(key_name="Kucoin_coin", data=coin)
            self.DATA_LOG.set_data(key_name="Kucoin_amount",data=coin_account)

            print("withdrawn ", result)
            is_withdrawn = True

        except Exception as e:
            print("Withdraw failed ", print(e))
            LOG.ArbitrageLog.error(e)
            is_withdrawn = False

        return is_withdrawn




    def _check_valr_funds(self, is_withdrawn, coin):
        """ After Kucoin has withdrawn, wait and check that it has arrived in Valr. """

        LOG.ArbitrageLog.info(f"Valr - Checking funds: {str(coin)}")

        if is_withdrawn != False:
            VALR_Funds_ready = self._wait_for_funds_VALR(coin)
        else:
            VALR_Funds_ready = False

        if VALR_Funds_ready == True:
            print("Funds have arived on valr: ", coin)
            LOG.ArbitrageLog.info(f"Valr - Funds arived on Valr: {str(coin)}")

        return VALR_Funds_ready




    def _execute_sell_coins_valr(self, coin):
        """ Execute a sell order on valr exchange after funs has arived in account from Kucoin."""

        print("Valr - Selling: ", coin)

        balances = self.valr.Valr_get_balances(type="main")
        available = balances[coin]["available"]

        LOG.ArbitrageLog.info(f"Valr - Selling: {str(coin)} to ZAR = {str(available)}")
        self.valr.SELL_coin_to_ZAR(amount_in_coins=available, 
                                   coin_pair=coin + "ZAR")

        sleep(5)
        ZAR_funds = False

        while ZAR_funds != True:

            ZAR_balance = self.valr.Valr_get_balances(type="main")["ZAR"]["available"]

            print("checking ZAR funds ", ZAR_balance)
            sleep(3)
            
            if float(ZAR_balance) >= float(500):
                LOG.ArbitrageLog.info(f"Sold = True | R{str(ZAR_balance)}")
                break

        # Set system to reverse arbitrage - we need to get the funds back to Kucoin at the cheapest cost.
        self.DATA_LOG.set_data(key_name="position", data="reverse_arbitrage")
        self.DATA_LOG.set_data(key_name="ZAR_funds", data=ZAR_balance)
        LOG.ArbitrageLog.info(f"Setting data: position=reverse_arbitrage")
        sleep(10)




    def _wait_for_funds_VALR(self, coins):
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




    def _wait_for_funds_KUCOIN(self, coin, acc_type):
        """ waits in a while loop until funds arive in the coins account. - KUCOIN """

        if coin == "XRP":
            check_amount = 50
        if coin == "AVAX":
            check_amount = 2
        if coin == "SOL":
            check_amount = 1
        else:
            check_amount = 1

        self.coin_account_value = False
        while self.coin_account_value != True:

            sleep(2)

            # Get all Kucoin Accounts
            all_accounts = self.kucoin.client.get_accounts()
            coin_account = self.kucoin.get_account(coin=coin, 
                                                   accounts=all_accounts, 
                                                   account_type=acc_type)

            print("kucoin - Checking Funds. - ", coin_account, coin)

            if coin_account != None:

                if float(coin_account["balance"]) >= check_amount:

                    self.coin_account_value = True
                    if self.coin_account_value == True:

                        print("KUCOIN - Funds True", coin)
                        break

        return True




    def _PRINT_arbitrage(self, coin, percent_difference, 
                        percent_increase, enough_usdc, USDT_balance):
        """ Simply Prints when an arbitrage oppertunity appears. """

        txt1 = coin
        txt2 = str(percent_difference) + "%"
        txt3 = " | R"+ str(percent_increase)
        txt4 = " | enough USDT: " + str(enough_usdc[0])
        txt5 =  " | USDT: : " + str(USDT_balance)

        print("\n*** Arbitrage oppertunity - ", txt1, txt2, txt3, txt4, txt5)




if __name__ == "__main__":

    algo_play = Algo_arbitrage()

    EXECUTE_TRADE = False
    WAIT_FOR_FUNDS_KUCOIN = False
    WAIT_FOR_FUNDS_VALR = False
    EXECUTE_SELL_COINS_VALR = False
    EXECUTE_TRADE_REVERSE = False

    if EXECUTE_TRADE == True:
        algo_play.execute_trade(coin="XRP")

    if WAIT_FOR_FUNDS_KUCOIN == True:
        print(algo_play.wait_for_funds_KUCOIN(coin="XRP", acc_type="main"))
