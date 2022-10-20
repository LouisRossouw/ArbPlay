import os

class Settings():
    """ A class to store all the settings for arb. """

    def __init__(self):
        """ Initialize trading settings. """

        # General
        self.Title = "ArbPlay"
        self.play_money = 10000
        self.force_signal = False, "XRP"     # Run tests on specific coin.
        self.print_statements = True

        self.position = "reverse_arbitrage" # "arbitrage" or "reverse_arbitrage" 
                                    # If the funds are on kucoin, this should be set to arbitrage to signal we need to send the funds to Valr
                                    # If the funds are on valr, this should be set to reverse_arbitrage to signal we need to send the funds to Kucoin.

        # Kucoin
        self.trade_account = "trade"        # use either "trade" or "main" accounts
        self.execute_withdrawels = False    # if True, withdraw / transfer coin to another wallet address.
        self.execute_order = False          # If True, then buy a coin using usdc
        self.execute_transfer = True


        # Valr
        self.valr_arbitrage_acc_name = "BOTARB"



        # Prices valuation
        self.percent_trigger = 1.7
        self.reverse_percent_trigger = 0.4