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

## How to use
1. 電源を入れる
2. PCのbluetoothをONにする
3. ターミナルで「ls ls /dev/tty.*」と入力して，デバイスを確認する．  
"/dev/tty.MindWaveMobile-DevA"とか出てくるはずなので，brainwave.pyの18行目のportの中身がこれになっているか確認する