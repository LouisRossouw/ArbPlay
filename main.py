from re import S
from time import sleep

import DripDrip.dripdrip as DP
import ArbitragePlay.run as ArbitragePlay
import Settings as SETTINGS

Drip = DP.DripDrip()
settings = SETTINGS.Settings()


while True:

    # Arbitrage
    if settings.arb_active == True:
        ArbitragePlay.run()

    # Dollar cost avaraging in valr.
    if settings.Drip_active == True:
        print("\nDrip:")
        Drip.run()


    sleep(8)



    

