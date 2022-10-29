import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Settings as SETTINGS

class LogLog():


    def __init__(self):


        self.SETTINGS = SETTINGS.Settings()




    def _logHandlers(self, LOGPATH):

        # create file handler which logs even debug messages
        fh = logging.FileHandler(LOGPATH)
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)




    def DripLog(self):

        LOGNAME = "DripLog"
        LOGPATH = "logs/DripLogs.log"

        # create logger
        self.logger = logging.getLogger(LOGNAME)
        self.logger.setLevel(logging.DEBUG)

        self._logHandlers(LOGPATH)

        self.logger.disabled = self.SETTINGS.logger_disabled

        return self.logger




    def ArbitrageLog(self):

        LOGNAME = "ArbitrageLog"
        LOGPATH = "logs/ArbitrageLogs.log"

        # create logger
        self.logger = logging.getLogger(LOGNAME)
        self.logger.setLevel(logging.DEBUG)

        self._logHandlers(LOGPATH)

        self.logger.disabled = self.SETTINGS.logger_disabled

        return self.logger





if __name__ == "__main__":

    log = LogLog()

    Driplog = log.DripLog()
    Driplog.error("hi")
    
    ArbitrageLog = log.ArbitrageLog()
    ArbitrageLog.info("arbitrageyay")

    try:
        os.ls(path)
    except Exception as e:
        Driplog.error(e)  

