import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from time import sleep
from arbMain import AlgoMain
import toolUtils.logger as LOG



logger = LOG.LogLog().DripLog()

def run():
    """ Runs the main app loop. """

    Aarbitrage_play = AlgoMain()
    print("---")
    
    try:
        Aarbitrage_play.run()
    except Exception as e:
        print(e)
        logger.error(e)
        sleep(10)

    print("---")




if __name__ == "__main__":
    run()

