﻿import socket
import select
import threading  # 標準入力はthreadでとりあえず

ipaddr = socket.gethostbyname(socket.gethostname())
port = 65000
bufsize = 4096
flag = True  # 終了する場合false


def send_std_input():
    while True:
        input_str = input()
        if input_str == "exit":
            flag = False
            s.send("sessionExit".encode('utf-16'))
            s.close()
            print("socket closed")
            exit()
        else:
            input_str += "\n"
            s.send(input_str.encode('utf-16'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    ipaddr = input("connect ipaddr:")
    
    # 接続
    s.connect((ipaddr, port))
    print("connected!!")
    # 受信スレッド
    inputTh = threading.Thread(target=send_std_input)
    inputTh.start()
    # exit入れるまで続ける
    while flag:
        # ソケットを監視
        # rready, wready, xready = select.select(readfds, [], [], 0)
        # # 受信が来たとき
        # for ready in rready:
        while True:
            chars = B""
            while True:
                recv = s.recv(bufsize)
                chars += recv
                if not len(recv) == bufsize :
                    print("recv:" + chars.decode('utf-16'))
                    break




