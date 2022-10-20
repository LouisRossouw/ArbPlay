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

        # Kucoin
        self.trade_account = "trade"        # use either "trade" or "main" accounts
        self.execute_withdrawels = False    # if True, withdraw / transfer coin to another wallet address.
        self.execute_order = False          # If True, then buy a coin using usdc
        self.execute_transfer = True


        # Valr
        self.valr_arbitrage_acc_name = "BOTARB"



        # Prices valuation
        self.percent_trigger = 0.5