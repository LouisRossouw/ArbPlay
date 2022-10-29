

class Settings():
    """ A class to store all the settings for ArbitragePlay. """

    def __init__(self):
        """ Initialize trading settings. """

# General

        self.Title = "ArbPlay"
        self.play_money = 10000
        self.print_statements = True

        # Kucoin
        self.trade_account = "trade"       # use either "trade" or "main" accounts
        self.execute_withdrawels = True    # if True, withdraw / transfer coin to another wallet address.
        self.execute_order = True          # If True, then buy a coin using usdc
        self.execute_transfer = True

        # Valr
        self.valr_arbitrage_acc_name = "BOTARB"
        self.execute_order_valr = True
        self.execute_withdrawels_valr = True




# ArbitragePlay.

        self.arb_active = True
        self.force_signal = False, "XRP"     # Run tests on specific coin.
        self.position = "reverse_arbitrage"  # "arbitrage" or "reverse_arbitrage" 
                                             # If the funds are on kucoin, this should be set to arbitrage to signal we need to send the funds to Valr
                                             # If the funds are on valr, this should be set to reverse_arbitrage to signal we need to send the funds to Kucoin
        # Prices valuation
        self.percent_trigger = 1.7
        self.reverse_percent_trigger = 0.4


# DripDrip - dollar cost avaraging bot.

        self.Drip_active = True
        self.days = 20
        self.invest_time = 20 # 8pm
        self.valr_DripDrip_acc_name = "BOT-DRIP"