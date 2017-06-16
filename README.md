# BrainWave

## Env.
* MacOS 10.10.5 over
* MindWaveManeger
* MindWaveDriver
* ThinkGearConnector

* Python 2.7.12 over
	* Only Python2.x
* NumPy 1.1.2 over
* Pyserial 3.1.1 over
* Thinkgear 0.2 over
* Matplotlib 1.5.3 over

## Run
$python brainwave.py

## brain_graph.py
### Run
$python brain_graph.py

## log
* 16/10/20: ver.1.0
* 16/10/24: ver.1.1;bag fix
* 16/12/05: add "How to use"

## How to use
1. 脳波センサ本体の電源を入れる
2. PCのbluetoothをONにする
3. ThinkGearConnectorを起動する
4. ターミナルで「ls /dev/tty.*」と入力して，デバイスを確認する．  
	* "/dev/tty.MindWaveMobile-DevA"とか出てくるはずなので，クラス"Mindwave()"の第一引数とする
5. ターミナルやSublimeText3からコードを実行する  
	* クラス "Mind(port, debug=True, attention=False, meditation=False)"の引数について
		* port: 接続ポート（"4."を参考に）
		* debug: デバッグ用のprint文を実行するかどうか（デフォルトはTrue）
		* attention: Attention値を取得するか（デフォルトはFalse）
		* meditation: Meditation値を取得するか（デフォルトはFalse）
	* SublimeText3でコードを実行する場合は，Command+b
	* ターミナルから実行する場合は，python brainwave.py
	* escで終了して，計測した脳波をcsv形式で書き出して保存する 
		* 10分に1回，バックアップとしてcsvを書き出します．ただし，このバックアップファイル名は単純なナンバリング（10分ごとに1, 2, 3となっていく）なので，スクリプトを停止した後にバックアップファイルを使う必要がある場合は避難させる/名前を変更する 
		* escで終了した場合，ファイル名にタイムスタンプが付くが，日付はつかないので要注意
6. 接続がうまくいかない場合，以下の方法を試す  
	* 脳波センサ本体の再起動  
	* PCのbluetoothの再起動（OFF→ON）  
	* Brainwave Visualizerを起動して，アプリと本体を一度接続して，うまくいったら接続解除（アプリ終了）してみる  
7. 禁止事項
	* スクリプト停止前に脳波センサの電源を切ること→フリーズします
	* スクリプト稼働中にPCと脳波センサがbluetooth圏外に移動する→フリーズします