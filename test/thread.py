import threading
import time


def hoge():
    while True:
        print("まんじ")
        time.sleep(1)


a = threading.Thread(target=hoge())
a.start()
while True:
    print("まじ")
    time.sleep(1)
