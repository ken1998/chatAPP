<?php

$port = 65000;
$process_stack = array();
$sockets = socket_create(AF_INET, SOCK_DGRAM, 0);
socket_set_nonblock($sockets);
socket_bind($s, '0.0.0.0', port);
socket_listen($s, 5);
/*
このへんでsend_socketとか配列作ってfork　送信専用プロセスを作成
mysql使うならたぶんいらない
*/

$socket =false;
#メインプロセスはソケット受付担当
#white(true)は怒られそうなので
while($pid != 0){
    $socket = socket_accept();
    if($socket != false){
        $process_stack[i] = pcntl_fork();
        #子プロセスのときprocess_stackが不要
        if($process_stack[i] == 0) break;
        $pid = $process_stack[i];
        $i++;
    }
}

#ここから子プロセスのsocket.recv監視、親プロセスへのデータ送信処理を書く予定でした
#mysql使うならここで親プロセスからのunixsock(プロセス間通信)も監視、send_dataを受け取り
#clientに送信する処理を受信処理のwhileに混ぜ込む(コスト知れてるから膨大にならない限り問題ないと思われる)

?>