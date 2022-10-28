from time import sleep

import DripDrip.dripdrip as DP
import ArbitragePlay.run as ArbitragePlay

Drip = DP.DripDrip()


while True:

    # Arbitrage
    ArbitragePlay.run()

    # Dollar cost avaraging in valr.
    Drip.run()


    sleep(8)



    

