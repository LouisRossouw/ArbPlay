import DripDrip.utils as utils

from data import Data_log
from settings import Settings

from kucoin_exchange import Kucoin
from valr_exchange import Valr

from arb import Algo_arbitrage
from arb_reverse import Algo_arbitrage_reverse



class AlgoMain():
    """ A class to store all the settings for algo play. """


    def __init__(self):
        """ Initialize algo settings. """

        self.kucoin = Kucoin()
        self.valr = Valr()
        self.SETTINGS = Settings()
        self.DATA_LOG = Data_log()

        self.Algo_arbitrage = Algo_arbitrage()
        self.Algo_arbitrage_reverse = Algo_arbitrage_reverse()

        self.TRADEPAIR_ALLOWED =  ["XRP", "SOL", "AVAX"]

        # Compatible trading pairs.
        self.VALR_COINPAIR = ["ETHZAR", "BTCZAR", "XRPZAR", "BNBZAR", 
                              "SOLZAR", "AVAXZAR", "SHIBZAR"]
                              
        self.KUCOIN_COINPAIR = ["ETH-USDC", "BTC-USDC", "XRP-USDC", 
                                "BNB-USDC", "SOL-USDC", "AVAX-USDC", "SHIB-USDC"]




    def run(self):
        """ Main trading algo happens here."""

        self.valr_data = self.valr.return_coinPair_group(coinpair_group=self.VALR_COINPAIR)
        kucoin_data = self.kucoin.return_coinPair_group(coinpair_group=self.KUCOIN_COINPAIR)
        
        rebalancing = self.DATA_LOG.return_data(key_name="rebalancing")

        if rebalancing == False:
            
            # Compare prices between 2 exchanges.
            return_analyse = self.compare(self.valr_data[0], kucoin_data)
            self.signal(return_analyse)

        if rebalancing == True:
            coin = self.DATA_LOG.return_data(key_name="coin_to_rebalance")
            self.SELL_coin_rebalance(coin=coin)




    def signal(self, return_analyse):
        """ Runs through the analyse data and if data is true, execute a True signal. """

        # the value that will trigger as an oppertunity, 
        # 4% price increase would trigger an abritrage for example.

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

                            # if the arbitrage spread is greater than. 
                            # then execute the trade from Kucoin to Valr.

                            if percent_difference >= percent_trigger:
                                self.Algo_arbitrage.execute_trade(allowed, 
                                                                  percent_difference, 
                                                                  growth_potential)

                        elif position == "reverse_arbitrage":

                            # if the reverse arbitrage spread is less than. 
                            # then execute the trade from Valr to Kucoin.

                            if percent_difference <= reverse_percent_trigger:
                                self.Algo_arbitrage_reverse.execute_trade_reverse(allowed, 
                                                                                  percent_difference, 
                                                                                  growth_potential)




    def SELL_coin_rebalance(self, coin):
        """ Wait for original coin price to == the current coin zar price on Kucoin to 
            make the sale, then the transfer is over and the aritrage cycle starts over.
        """

        print("Rebalancing --")

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
                                    data=False)




    def compare(self, exchange_local, exchange_international):
        """ Compares the price difference betweem local and international. """

        data = {}
        print(self.DATA_LOG.return_funds_position())
        kucoin_fiat_prices = self.kucoin.get_fiat_price_for_coin(fiat="ZAR")

        # i can buy at kucoin int_ask and sell at valr loc_bid
        for i in range(len(exchange_local)):

            loc_currencyPair = exchange_local[i]["currencyPair"]
            loc_bid = exchange_local[i]["bidPrice"]
            int_currencyPair = exchange_international[i]["symbol"]
            coin = int_currencyPair.split("-")[0]
            int_coin_zar = kucoin_fiat_prices[coin]

            return_analyse = self.analyse(loc_bid, int_coin_zar, loc_currencyPair)
            data[loc_currencyPair] = return_analyse

        return data




    def analyse(self, loc_bid, int_coin_zar, loc_currencyPair):
        """ Check the spread if its large enough to let an execution buy and sell. """

        percent_difference = round(utils.get_percentage_difference(loc_bid, 
                                                                   int_coin_zar), 2)
        percent_increase = round(utils.percent_increase(percent_difference, 
                                                        self.SETTINGS.play_money), 3)

        self.print_statement(loc_bid, 
                             int_coin_zar, loc_currencyPair, 
                             percent_difference, percent_increase)

        return percent_difference, percent_increase




    def print_statement(self, loc_bid, int_coin_zar, loc_currencyPair, percent_difference, percent_increase):
        """ Prints out. """

        txt1 = loc_currencyPair
        txt2 = " |  R "+str(percent_increase)
        txt3 = " | "+str(percent_difference) + "%"
        txt4 = " | Valr price R"+ str(loc_bid)
        txt5 = " | Kucoin price R"+str(round(float(int_coin_zar), 2))

        if self.SETTINGS.print_statements == True:
            print(txt1, txt2, txt3, txt4, txt5)












if __name__ == "__main__":

    algo_play = AlgoMain()

    RUN = True
    SIGNAL = False
    ANALYSE = False
    COMPARE = False
    PRINT_STATEMENT = False

    if RUN == True:
        algo_play.run()

    if PRINT_STATEMENT == True:
        algo_play.print_statement(18, 17, "XRPZAR", 5, 6)

    if ANALYSE == True:
        print(algo_play.analyse(19, 18, "XRPZAR", "XRP-USDC"))

    if SIGNAL == True:
        return_analyse = algo_play.compare(algo_play.valr_data[0], algo_play.kucoin_data)
        algo_play.signal(algo_play.valr_data[0], algo_play.kucoin_data)

    if COMPARE == True:
        VALR_COINPAIR = ["ETHZAR", "BTCZAR", "XRPZAR", "BNBZAR", "SOLZAR", "AVAXZAR", "SHIBZAR"]
        KUCOIN_COINPAIR = ["ETH-USDC", "BTC-USDC", "XRP-USDC", "BNB-USDC", "SOL-USDC", "AVAX-USDC", "SHIB-USDC"]
        valr_data = algo_play.valr.return_coinPair_group(coinpair_group=VALR_COINPAIR)
        kucoin_data = algo_play.kucoin.return_coinPair_group(coinpair_group=KUCOIN_COINPAIR)
        algo_play.compare(algo_play.valr_data[0], algo_play.kucoin_data)

