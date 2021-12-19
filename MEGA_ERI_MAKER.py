import os
import gophergrades
import rmp
import sys
import time
import threading
#Spinner class taken from:https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '/-\\|/-\\|/': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            x=next(self.spinner_generator)
            sys.stdout.write(x)
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()
            

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

    ##need dataset, I used an online converter and got the file from:
    #https://github.com/DannyG72/UMN-Grade-Dataset/blob/master/raw_grade_data_summer2017_summer2020.xlsx
fname = input("dataset file name: ")
with Spinner():

    gophergrades.write_data(fname) #dataset.xlsx->temp_data.eri
##    print("got temp eri file")

    print("getting proffessor data from rmp (this will take over an hour)") #can I speed it up, maybe???

    rmp.write() # temp_data.eri->data.eri
    print("got data.eri file")


    ##os.remove('gg.csv')
    ##os.remove('temp_data.eri')
    ##os.remove('profs.txt')
    ##os.remove('links.txt')
    ##print("removed temp files")
    input("press enter to quit")
