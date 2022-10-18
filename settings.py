import os

class Settings():
    """ A class to store all the settings for arb. """

    def __init__(self):
        """ Initialize trading settings. """

        # General
        self.Title = "ArbPlay"
        self.play_money = 100000
        self.print_statements = True

        # Kucoin
        self.execute_withdrawels = False # if True, withdraw / transfer coin to another wallet address.
        self.execute_order = False # If True, then buy a coin using usdc


        # Valr
        self.valr_arbitrage_acc_name = "BOTARB"



        # Prices valuation
        self.percent_trigger = 1.5