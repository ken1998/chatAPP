import socket
import select
import threading #標準入力はthreadでとりあえず

ipaddr = "172.0.0.1"
port = 65534
bufsize = 4096
flag = True #終了する場合false


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    #接続
    s.connect((ipaddr, port))
    print("connected!!")
    #監視対象ソケットに追加(clientなので一つ)
    readfds = set([s])
    inputTh = threading.Thread(target=sendStdInput, name="inputTh", args=())
    inputTh.start()

    #exit入れるまで続ける
    while(flag):
        #ソケットを監視
        rready, wready, xready = select.select(readfds, [], [])
        #受信が来たとき
        for ready in rready:
            recv = ""
            while(True):
                len = ready.recv(bufsize)
                recv += len
                if len != bufsize :
                    break
            print (recv.decode())

def sendStdInput():
    
