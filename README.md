# BrainWave

## Env.
* MacOS 10.10.5 over
* MindWaveManeger
* MindWaveDriver
* ThinkGearConnector

* Python 2.7.12 over
* NumPy 1.1.2 over
* Pyserial 3.1.1 over
* Thinkgear 0.2 over
* Matplotlib 1.5.3 over

## Run
$python brainwave.py

## brain_graph.py
### Run
$python brain_graph.py filename  
asterisk without ".csv"

## log
* 16/10/20: ver.1.0
* 16/10/24: ver.1.1;bag fix
* 16/12/05: add "How to use"

## How to use
1. 電源を入れる
2. PCのbluetoothをONにする
3. ターミナルで「ls /dev/tty.*」と入力して，デバイスを確認する．  
"/dev/tty.MindWaveMobile-DevA"とか出てくるはずなので，brainwave.pyの18行目のportの中身がこれになっているか確認する
4. ターミナルやSublimeText3からコードを実行する
* enterでフラグ切り替え（録音開始・停止のタイミングとかで使用可能）
* escで終了して，計測した脳波をcsv形式で書き出して保存する
5. 接続がうまくいかない場合，以下の方法を試す
*本体の再起動
*PCのbluetoothの再起動（OFF→ON）
*Brainwave Visualizerを起動して，アプリと本体を一度接続して，うまくいったら接続解除（アプリ終了）してみる