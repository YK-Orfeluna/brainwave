# -*- coding: utf-8 -*
import sys
import numpy as np
import pandas as pd

v = sys.version_info[0]
if v == 2 :
	import Tkinter
	import tkMessageBox
	import tkFileDialog
elif v == 3 :
	import tkinter as Tkinter
	from tkinter import messagebox as tkMessageBox
	from tkinter import filedialog as tkFileDialog
else :
	exit("*This script only supports Python2.x or 3.x.\nSorry, we can not support your Python.")


### GUI用のおまじない
root = Tkinter.Tk()
root.option_add('*font', ('FixedSys', 14))
fTyp=[('csvファイル','*.csv')]
iDir='.'


### ファイル選択
lb=Tkinter.Label(root, text="Chose answer-file",width=20)
lb.pack()

filename = tkFileDialog.askopenfilename(filetypes=fTyp,initialdir=iDir)

if filename == "" :
	exit("*You did not select your csv files")
else :
	print("*The file you selected: %s" %filename)

### データ読み込み
df = pd.read_csv(filename, index_col=None, encoding="utf-8")
data = df.values
data = data.T
labels = df.columns.values[2:]

x = data[1]
COLORS = ["blue", "green", "red", "cyan", "purple", "orange", "black", "gray"]


import matplotlib.pyplot as plt

plt.figure()
# marker引数で，マーカーを指定可能．Flaseで解除可能．
# linewidth引数で，線の太さを指定可能
for i, y in enumerate(data[2:]) :
	plt.subplot(4, 2, i+1)
	plt.plot(x, y, label=labels[i], linewidth=2, marker="o", color=COLORS[i])
	plt.xlabel("sec.")
	#plt.ylim(0, 50000)			# グラフのy軸の描画範囲を決定する(min, max)．コメントアウトで範囲自動決定
plt.show()
sys.exit()