import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import toolUtils.utils as utils
from Settings import Settings


class Data_log():
    """ A class for data movement. """

    def __init__(self):
        """ Initialize data settings. """

        self.SETTINGS = Settings()

        self.data_path = self.return_arbitrage_trade()
        self.data_file = utils.read_json(self.data_path) 




    def return_arbitrage_trade(self):
        """ returns the path to the arbitrage json file. """

        this_file = os.path.dirname(os.path.abspath(__file__))
        data_file = f"{this_file}/data/arbitrage.json"

        if os.path.exists(data_file) != True:
            data = {}
            utils.write_to_json(data_file, data)

        return data_file




    def return_data(self, key_name):
        """ Generic return data for key. """
        
        data = utils.read_json(self.data_path)[key_name]
        return data




    def set_data(self, key_name, data):
        """ Generic data input. """

        self.data_file[key_name] = data
        utils.write_to_json(self.data_path, self.data_file)  





if __name__ == "__main__":

    data_log = Data_log()

    print(data_log.return_arbitrage_trade())
