import time


def log(message):
    print(time.asctime(time.localtime()), ':', message, end='\n\n')
