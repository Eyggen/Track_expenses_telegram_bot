from time import sleep
from datetime import datetime


def clock():
    while True:
        sleep(60)
        now_time = datetime.now()
        data = now_time.strftime("%Y-%m-%d")
        print(data[8:10])
        if data[8:10] == '01':
            sleep(86400)
