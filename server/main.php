<?php

$port = 65000;
$process_stack = array();
$sockets = socket_create(AF_INET, SOCK_DGRAM, 0);
socket_set_nonblock($sockets);
socket_bind($s, '0.0.0.0', port);
socket_listen($s, 5);
while(true){
    $socket = socket_accept();
    if($socket == false){

    }



}



?>