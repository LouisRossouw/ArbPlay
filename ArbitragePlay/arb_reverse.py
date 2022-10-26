import math
import DripDrip.utils as utils
from time import sleep

from data import Data_log
from settings import Settings

from kucoin_exchange import Kucoin
from valr_exchange import Valr


class Algo_arbitrage_reverse():
    """ A class to store all the settings for algo play. """


    def __init__(self):
        """ Initialize algo settings. """

        self.kucoin = Kucoin()
        self.valr = Valr()
        
        self.SETTINGS = Settings()
        self.DATA_LOG = Data_log()




    def _PRINT_arbitrage(self, coin, percent_difference):
        """ Simply Prints when an arbitrage oppertunity appears. """

        txt1 = coin
        txt2 = str(percent_difference) + "%"

        print("\n*** Arbitrage oppertunity - ", txt1, txt2)




    def _Check_enough_ZAR(self):    
        """ check if enough ZAR in account. """

        ZAR_balance = (self.valr.Valr_get_balances(type="main")["ZAR"]["available"]).split(".")[0]

        if float(ZAR_balance) >= float(1000):
            enough_ZAR = True
        else:
            enough_ZAR = False

        return ZAR_balance, enough_ZAR




    def _execute_buy_COIN(self, coin, ZAR_balance):
        """ If enough ZAR exists, then buy coins. """

        print("VALR - BUY ", coin, " R", ZAR_balance)

        # Get coins askPrice to store in data for later.
        market_data = self.valr.Valr_client.get_market_summary()
        coin_askPrice = self.valr.return_coinPair_data(coinpair=coin+"ZAR", 
                                                       market_data=market_data)["askPrice"]

        amount_coins_buy = float(float(ZAR_balance) / float(coin_askPrice))
        rounded_coins = math.floor(amount_coins_buy * 100)/100.0
        self.valr.BUY_ZAR_to_coin(amount_in_coins=rounded_coins, coin_pair=coin+"ZAR")


        self.DATA_LOG.set_valr_coin_askPrice(coin_price_ZAR=coin_askPrice)
        self.DATA_LOG.set_valr_coin_amount(coin_amount=rounded_coins)




    def _wait_for_coins(self, coin):
        """ after buying coins, wait / make sure it exists before proceeding. """

        while True:
            COIN_balance = self.valr.Valr_get_balances(type="main")[coin]["available"]
            print("VALR - Checking coin Balance ", COIN_balance, coin)
            sleep(2)
            if float(COIN_balance) >= float(1):
                enough_COIN = True
                break

        return enough_COIN




    def _valr_withdraw_info(self, coin):
        """ Withdrawn information from valr. """

        withdraw_info = self.valr.Valr_client.get_crypto_withdrawal_info(currency_code=coin)

        isActive = withdraw_info["isActive"]
        withdrawalDecimalPlaces = withdraw_info["withdrawalDecimalPlaces"]
        withdrawCost = withdraw_info["withdrawCost"]
        supportsPaymentReference = withdraw_info["supportsPaymentReference"]
        minimumWithdrawAmount = withdraw_info["minimumWithdrawAmount"]




    def _execute_valr_withdraw(self, coin):
        """ Withdraw coin from valr to Kucoin address. """

        print("VALR - WITHDRAW to Kucoin ", coin)
        executed = False
        # return kucoin wallet address for coin
        kucoin_coin_wallet_data = self.kucoin.get_deposit_address(coin=coin)
        if bool(kucoin_coin_wallet_data) != False:

            kucoin_address = kucoin_coin_wallet_data[0]["address"]
            kucoin_memo = kucoin_coin_wallet_data[0]["memo"]
            kucoin_chain = kucoin_coin_wallet_data[0]["chain"]

            COIN_balance = self.valr.Valr_get_balances(type="main")[coin]["available"]
            round_amount = math.floor(float(COIN_balance) * 100)/100.0

            print("VALR - Withdrawing ", round_amount, kucoin_address)
            print("to KUCOIN - ", kucoin_address, kucoin_memo, kucoin_chain)

            pay = self.valr.Valr_client.post_crypto_withdrawal(currency_code=coin, 
                                                            amount=round_amount,
                                                            address=kucoin_address,
                                                            payment_reference=kucoin_memo
                                                            )
            executed = True
        
        return executed




    def _inner_trasfer(self, coin):
        """ Transfer coins from main to trade account to be ready to sell. """

        print("KUCOIN - Selling to USDT.")
        all_accounts = self.kucoin.client.get_accounts()
        coin_account = self.kucoin.get_account(coin=coin, 
                                                accounts=all_accounts, 
                                                account_type="main")

        coin_balance = coin_account["balance"]

        # transfer to trade account to sell.
        self.kucoin.inner_transfer(coin=coin, 
                                   from_account="main", 
                                   to_account="trade", 
                                   amount_coins=coin_balance)

        return True




    def SELL_coin_rebalance(self, coin):
        """ Wait for original coin price to == the current coin zar price on Kucoin to 
            make the sale, then the transfer is over and the aritrage cycle starts over.
        """
        while True:
            sleep(5)
            print("--")

            valr_coin_askPrice = self.DATA_LOG.return_valr_coin_askPrice()

            fiat_prices = self.kucoin.get_fiat_price_for_coin(fiat="ZAR")
            kucoin_coin_value = fiat_prices[coin]

            percentage_difference = utils.get_percentage_difference(kucoin_coin_value, 
                                                                    valr_coin_askPrice)
            valr_coin_amount = self.DATA_LOG.return_data("valr_coin_amount")

            current = float(valr_coin_amount) * float(kucoin_coin_value)
            valr_cur = float(valr_coin_amount) * float(valr_coin_askPrice)

            # for print statements.
            VLRrcn_pr = str(round(float(valr_coin_askPrice),2))
            KCcn_pr = str(round(float(kucoin_coin_value),2))
            prcnt = str(round(float(percentage_difference),2))
            crnt = str(round(float(current),2))  
            vlr_cnnt = str(round(float(valr_cur),2)) 

            print("KUCOIN - Waiting to sell: ","R"+str(VLRrcn_pr), KCcn_pr, prcnt+"%", "R"+str(crnt), " R"+str(vlr_cnnt))

            if float(kucoin_coin_value) >= float(valr_coin_askPrice):

                accounts = self.kucoin.client.get_accounts()
                amount_coins = self.kucoin.get_account(coin=coin, 
                                                       accounts=accounts, 
                                                       account_type="trade")["balance"]

                print("KUCOIN - selling: ", amount_coins)
                self.kucoin.sell_coin(coin+"-USDT", amount_in_coins=amount_coins)

                self.DATA_LOG.set_fund_position(position="arbitrage")
                self.DATA_LOG.set_data(key_name="rebalancing", 
                                       data=True)




    def execute_trade_reverse(self, coin, percent_difference, percent_increase):
        """ Run the reverse - execution of the trade between the exchanges. VALR TO KUCOIN. """

        enough_COIN = False # TEST -  CHANGE THIS BACK TO FALSE WHEN IM DONE TESTING !
        funds_arived = False
        execute_valr_orders = self.SETTINGS.execute_order_valr
        execute_valr_withdraws = self.SETTINGS.execute_withdrawels_valr

        self._PRINT_arbitrage(coin, percent_difference)

        # 1. check if enough ZAR in account.
        enough_ZAR = self._Check_enough_ZAR()
            
        # BUY coin with ZAR.
        if enough_ZAR[1] == True:
            if execute_valr_orders == True:

                # Buy coin.
                self._execute_buy_COIN(coin=coin, 
                                       ZAR_balance=enough_ZAR[0])

                # Check if coins exist.
                enough_COIN = self._wait_for_coins(coin)

                self.DATA_LOG.set_data(key_name="coin_to_rebalance", 
                                       data=str(coin))
        
        if enough_COIN == True:
            if execute_valr_withdraws == True:

                # Withdraw coins to Kucoin.
                self._execute_valr_withdraw(coin)

                # Wait for funds to arive.
                funds_arived = self.wait_for_funds_KUCOIN(coin=coin, 
                                                          acc_type="main")

        # Transfer coins from main to trade account to be ready to sell.
        if funds_arived == True:

            status = self._inner_trasfer(coin=coin)

            self.DATA_LOG.set_data(key_name="rebalancing", data=True)




    def wait_for_funds_KUCOIN(self, coin, acc_type):
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






if __name__ == "__main__":

    algo_play = Algo_arbitrage_reverse()

    EXECUTE_TRADE = False
    WAIT_FOR_FUNDS_KUCOIN = False
    WAIT_FOR_FUNDS_VALR = False
    EXECUTE_SELL_COINS_VALR = False
    EXECUTE_TRADE_REVERSE = False

    EXECUTE_VALR_WITHDRAW = False

    if EXECUTE_TRADE == True:
        algo_play.execute_trade(coin="XRP")

    if WAIT_FOR_FUNDS_KUCOIN == True:
        print(algo_play.wait_for_funds_KUCOIN(coin="XRP", acc_type="main"))

    if EXECUTE_VALR_WITHDRAW == True:
        algo_play._execute_valr_withdraw(coin="AVAX")