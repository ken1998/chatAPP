# chatAPP

## 概要

C/Sで動作する1対多で動作するチャットアプリです。
python3.7で開発を行っています。
特徴としては、
・socketを使用（TCP）
・DBを使用せず共有メモリ(multiprocessing)を利用
・セッションをforkを利用し、1セッション1プロセスで管理
です。

## 起動方法

python3 server.py
python3 client.py
をサーバー・クライアントで実行してください。
・注意点
サーバーのポートは65000でbindしているのでFWの設定をお願いします。
fork命令が動作する環境（linuxなど）でサーバーを実行してください。

## 操作方法

サーバーを起動
クライアント起動時にIPを聞かれるのでサーバーを起動したPCのIPを入力
connectedと出力されるのでそのまま入力してenterで送信
(配列確保の数の都合上70文字くらいまでです、サロゲートペアを使うともっと減ります)
exitと入力すると終了します

## バグ

### server

送信回数が合計150回を超えるとバグります(再確保のコード未制作)
waitpidを挟んでいないのでコネクションを終了した後もゾンビプロセスが残ります(killが必要になる可能性あり)

### client
serverが先に死ぬとバグります(強制切断の検知をしていない)

# 以後過去の遺産

## なぜ作ろうとしているのか
先日ゲーム科の学校の先生に、ゲームサーバに関する知識をつけたいと相談したところ  
「最近TCPでかなり作ってるし複数人で使えるチャットサーバー辺り作ってみたら良いよ、ノンブロッキングとかも勉強してきて」  
とお声を頂いたので作ることにしました。  

## 仕様


### クライアント
ノンブロッキングを勉強しておいでと聞いているのでソケットをselectで監視し、受信を行う。
言語はGUIの関係でC#が有力
ノンブロッキングモードで自力で書くべきなのかはまだ良くわかっていない（そのうち書きます)  
追記3/6　とりあえずpython(CUI)で書きました

### サーバー
コネクション数が増えていくのでとりあえずforkでの処理を勉強してみようかと  
~~言語はPHPの予定(ワンチャンCPP)~~男気CPP決めます(深夜テンション)  
追記3/6  MySQLやらsqlite辺り使えば割と簡単にできそうだが使いたくないしforkだけで実装するのは（主にプロセス間通信が)苦痛すぎるのでPHPやめます、EPOLLさんはまたの機会に
