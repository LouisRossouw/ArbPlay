from time import sleep

from algo_play import Algo_play



def run():
    """ Runs the main app loop. """

    time_delay = 8

    Aarbitrage_play = Algo_play()


    while True:

        print("---")
        
        Aarbitrage_play.run()

        print("---")
        sleep(time_delay)









if __name__ == "__main__":

    run()