from time import sleep

# from algo_play import Algo_play
from arbMain import AlgoMain



def run():
    """ Runs the main app loop. """

    time_delay = 8

    Aarbitrage_play = AlgoMain()


    while True:

        print("---")
        
        try:
            Aarbitrage_play.run()
        except Exception as e:
            print(e)
            input()


        print("---")
        sleep(time_delay)









if __name__ == "__main__":

    run()