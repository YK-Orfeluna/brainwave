# -*- coding: utf-8 -*
"""
=========================================================
                    BrainWave to Graph                      
=========================================================
This system is developed by Python 2.7.12 & Numpy1.1.2 & Matplotlib1.5.3.
(c) 2016 Yuki Kitagishi
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

# コマンドライン引数で，csvファイルの日付部分を指定可能
# $python brain_graph.py XXXXXXXXX
# XXXXXXXXXの部分が日付
args = sys.argv
if len(args) == 1 :
	csv = "test/brainwave_20161015162019.csv"
else :
	csv = "brainwave_" + args[1] + ".csv"
data = np.genfromtxt(csv, delimiter=",")

x = np.arange(len(data))
label = ["Delta", "Theta", "Low_Alpha", "High_Alpha", "Low_Beta", "High_Beta", "Low_Gamma", "High_Gamma"]
color = ["blue", "green", "red", "cyan", "purple", "orange", "black", "gray"]

plt.figure()
# marker引数で，マーカーを指定可能．Flaseで解除可能．
# linewidth引数で，線の太さを指定可能
for i, c in enumerate(color) :
	plt.plot(x, data[:, i+3], label=label[i], linewidth=2, marker="o", color=c)

plt.xlabel("sec.")
#plt.ylim(0, 50000)			# グラフのy軸の描画範囲を決定する(min, max)．コメントアウトで範囲自動決定
plt.title(csv)
plt.legend(loc=2)			# 凡例の表示と場所(loc）を設定する

plt.show()
sys.exit()

