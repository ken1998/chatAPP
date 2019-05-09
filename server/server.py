import socket
import threading
import os
import array
import multiprocessing as mp
import pdb
"""
こんなものなかった:
    子プロセスに送信する文字列を渡すのに使用
    rpipe, wpipe = Pipe()
    子プロセスが受信したものを集約するのに使用
"""
pid = 0


class ShareMemory:
    latest = mp.Value('I', 0)  # 共有変数　0から149まで　最新配列の添字を格納
    where_loaded = 0  # ローカル　clientに送った配列の添字を保持
    str1 = []
    str2 = []
    str3 = []
    share_str = []

    def __init__(self):
        for i in range(50):
            self.str1.append(mp.Array('B', 150))
            self.str2.append(mp.Array('B', 150))
            self.str3.append(mp.Array('B', 150))
            self.share_str = [self.str1, self.str2, self.str3]
    # share_str->str[1~3]->array[0~49]->char(list構造)　で取り出す

    """
    get_array:引数(int) 返り値 mp.Array
    引数に応じたarrayをshare_strから呼び出し返却する
    """
    def get_array(self, number: int):
        # ちゃんと例外にしたい
        if number >= 150:
            print("範囲外参照")
            print(number)
        str_list = self.share_str[int(number / 50)]
        str_array = str_list[int(number % 50)]
        return str_array

    """
    store:引数(byte) 返値 none
    入力されたbyteをlatestに記されたarrayにunsigned charに変換、格納する
    すでに入力されていた場合は一度空にする
    """
    def store(self, utf16_string: bytes):
        with self.latest.get_lock():
            self.latest.value += 1
            if self.latest.value >= 150:
                self.latest.value == 0
            target = self.get_array(self.latest.value)
#        if len(target) != 0:
            with target.get_lock():
                temp = array.array('B')
                temp.frombytes(utf16_string)
                # clearがmp.arrayになかったのでゆっくり考えます
                # delしてarrayをlistに確保し直す可能性
    #            target.clear()
                store_debug = B""
                for hoge in temp:
                    store_debug += hoge.to_bytes(1, 'big')
               # print("store:" + store_debug.decode('utf-16'))
                print("store_byte:" + str(store_debug))
                i = 0
                for hoge in temp:
                    print("now_store:" + str(hoge))
                    target[i] += hoge
                    i += 1
                

    """
    load:引数(int) 返値 bytes
    入力されたintが示すarrayに格納されたcharをbytesに結合し返却する
    """
    def load(self, number: int):
        target = self.get_array(number)
        join = B''
        chars = B''
        is_2byte = False  # 今のループが2バイト目か
        byte_num = 0
        loop = True
        # pdb.set_trace()
        while loop:
            # 進捗　targetの指定の仕方があやしい
            # 読みだしたものを全部取得する
            chars += target[byte_num].to_bytes(1, 'big')
            # 2バイト分だけ保持する（1文字分）
            join += target[byte_num].to_bytes(1, 'big')
            if is_2byte:
                # ヌル文字で終了
                if chars == "\n".encode('utf-16le'):
                    loop = False
                is_2byte = False
                chars = B""
            else:
                is_2byte = True
            byte_num += 1

        print("loaded:" + join.decode('utf-16'))
        return join

    """
    load_until_latest:引数 none 返り値 list[bytes]
    where_loadとlatestを比較し、latestまでを返す
    where_load == latest
    """
    def load_until_latest(self):
        return_list = []
        # 最新まで読み込んだら終了する
        while self.latest.value != self.where_loaded:
            return_list.append(self.load(self.where_loaded + 1))
            self.where_loaded += 1
            if self.where_loaded >= 150:
                self.where_loaded = 0
            # 一回余分にインクリメントしてるので引く
            # self.where_loaded -= 1
        return return_list


class TcpChatServer:
    process_lists = []
    ipaddr = socket.gethostbyname(socket.gethostname())
    port = 65000
    bufsize = 4096
    conn: socket
    sm: ShareMemory

    def __init__(self, share_memory: ShareMemory):
        self.sm = share_memory

    def fork_sock(self):
        await_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("this server IP is " + self.ipaddr)
        await_socket.bind(("0.0.0.0", self.port))
        await_socket.listen(5)
        pflag = True
        while pflag:
            try:
                # 接続要求を受信
                self.conn, addr = await_socket.accept()
                print("connect from:" + addr[0])
                # ロード同期を最新からに設定
                self.sm.where_loaded = self.sm.latest.value
                global pid
                pid = os.fork()
                print("forking")
                # 子プロセスなら終了
                if pid == 0:
                    # 子プロセスに基本ソケットは不要
                    await_socket.close()
                    print("clone number:" + str(self.sm.latest.value))
                    pflag = False
                # forkerror
                elif pid == -1:
                    exit(1)
                # 親プロセスに子ソケットも不要
                else:
                    print("host process")
                    self.process_lists.append(pid)
                    self.conn.close()
            except KeyboardInterrupt:
                exit(0)

    """
    recive_message:引数 none 返り値 bytes
    クライアントからの受信を格納する
    """
    def receive_message(self):
        # pdb.set_trace()
        while True:
            char = B''
            while True:
                receive = self.conn.recv(4096)
#                char += receive
#                if len(receive) == 0:
                # 終了命令がきたらこのプロセスを終了する
                if receive.decode('utf-16') == "sessionExit":
                    self.conn.close()
                    exit()
                sm.store(receive)
                print("received:" + receive.decode('utf-16'))
                break

    def send_message(self, message: bytes):
        self.conn.send(message)


if __name__ == "__main__":
    sm = ShareMemory()
    server = TcpChatServer(sm)
    # 親プロセスはfork_sockで着信を待ち続ける
    server.fork_sock()
    # ここから子プロセス
    print("forked")
    # 受信を別スレッドで行う
    recv_thread = threading.Thread(target=server.receive_message)
    print("made thread")
    recv_thread.start()
    print("thread_start")
    while True:
        if sm.latest.value != sm.where_loaded:
            print("main process:sending")
            loads = sm.load_until_latest()
            print(loads)
            print("main process:loaded")
            for load in loads:
                print(load)

            print(load.decode('utf-16'))
            server.send_message(load)



    # acceptをメイン、sendとrecvを子プロセスで管理
    # pipeか共有メモリを使うか、一つ作成するかプロセス毎に作成するか
