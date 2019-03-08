import socket
import threading
import os
from multiprocessing import Queue

# 子プロセスに送信する文字列を渡すのに使用
rpipe, wpipe = Pipe()
# 子プロセスが受信したものを集約するのに使用
q = multiprocessing.Queue()
pid = 0

class TcpChatServer:
    self.process_lists = []
    self.ipaddr = "172.0.0.1"
    self.port = 65000

    def __init__(self):
        pass

    def forksock(self):
        await_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await_socket.bind(("0.0.0.0", port))
        await_socket.listen(5)
        while True:
            try:
                # 接続要求を受信
                conn, addr = await_socket.accept()
                print("connect from:" + addr)
                global pid
                pid = os.fork()
                # 子プロセスなら終了
                if pid == 0:
                    # 子プロセスに基本ソケットは不要
                    await_socket.close()
                    break
                # forkerror
                elif pid == -1:
                    exit(1)
                # 親プロセスに子ソケットも不要
                else:
                    self.process_lists.append(pid)
                    conn.close()
            except KeyboardInterrupt:
                exit(0)

    def recv_chat(self):
        pass

    def send_message(self):
        pass


if __name__ == "__main__":
    server = TcpChatServer()
    server.forksock()

    # acceptをメイン、sendとrecvを子プロセスで管理
    # pipeか共有メモリを使うか、一つ作成するかプロセス毎に作成するか