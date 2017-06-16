# -*- coding: utf-8 -*

import time, sys
if sys.version_info[0] == 2 :
	import thinkgear		# Pyserialが必要
else :
	exit("*This script only supports Python2.x.\nSorry, we can not support your Python.")

import numpy as np
#import cv2
import pandas as pd

import key_num as key

WINDOWNAME = "MindWave"

STR_1 = "ASIC EEG Power: EEGPowerData("
STR_2 = ")"
STR_3 = ", "
STR_A = "ATTENTION eSense: "
STR_M = "MEDITATION eSense: "

NAME = np.array(["delta=", "theta=", "lowalpha=", "highalpha=", "lowbeta=", "highbeta=", "lowgamma=", "midgamma="])

def stamp() :
	t = time.localtime()
	stamp = [t.tm_hour, t.tm_min, t.tm_sec]
	out = ""
	for i in stamp :
		s = str(i)
		if i < 10 :
			s = "0" + s
		out += s
	return out

class Mind() :
	def __init__(self, port, debug=True, attention=False, meditation=False) :
		self.DEBUG = debug
		self.ATTENTION = attention
		self.MEDITATION = meditation
		
		self.label = np.array(["Unix", "TimeStamp", "Delta", "Theta", "Low_Alfa", "High_Alfa", "Low_Beta", "High_Beta", "Low_Gamma", "Mid_Gamma"])
		if attention :	
			self.label = np.append(self.label, "Attention")
		if meditation :
			self.label = np.append(self.label, "Meditation")

		self.param = {"port":port, "debug":debug, "attention":attention, "meditation":meditation}
		if debug :
			print(self.param)

		self.img1 = np.zeros([500, 500, 1])
		self.brain = np.zeros([1, self.label.shape[0]])

		self.th = thinkgear.ThinkGearProtocol(port)		# 接続
		self.think = self.th.get_packets()
		print(self.think)		

	def brainwave(self) :
		p = self.psd

		p = str(p)					# pをstrに変換
		p = p.lstrip(STR_1)			# pから余分な文字を取り除く
		p = p.rstrip(STR_2)
		p = p.split(STR_3)			# pを", "で区切ってlist形式に

		t = time.localtime()

		self.time_brain = time.time()
		result = [time.time(), stamp()]
		for x, i in enumerate(p) :
			out = i.lstrip(NAME[x])
			result.append(out)

		if self.ATTENTION :
			result.append(self.attention.lstrip(STR_A))
		if self.MEDITATION :
			result.append(self.meditation.lstrip(STR_M))
	
		out = np.array([result])
		if self.DEBUG :
			print(out)
		return out

	def csv(self, name="brain"+str(stamp())) :							# CSV形式で保存
		df = pd.DataFrame(self.brain[1:], columns=self.label)
		df.to_csv(name+".csv", index=False, encoding="utf-8")

	def finish(self) :						# 終了処理
		#cv2.destroyAllWindows()
		self.th.io.close()
		self.th.serial.close()
		sys.exit("System Exit")

	def main(self) :
		print("System Beginning")

		start_time = time.time()
		csv_flag = 1
		cnt = 0

		attention = meditation = ""

		for packets in self.think:
			for p in packets:
				if isinstance(p, thinkgear.ThinkGearRawWaveData):		# Rawデータを取り除く
					continue

				if isinstance(p, thinkgear.ThinkGearPoorSignalData):	# Poorシグナルを取り除く	
					continue

				if isinstance(p, thinkgear.ThinkGearAttentionData):		# Attention値を取り除く
					if self.ATTENTION :
						self.attention = str(p)
						cnt += 1
					else :
						continue					

				if isinstance(p, thinkgear.ThinkGearMeditationData):	# Meditation値を取り除く
					if self.MEDITATION :
						self.meditation = str(p)
						cnt += 1
					else :
						continue

				if isinstance(p, thinkgear.ThinkGearEEGPowerData):		# フーリエ変換されたデータを取り除く	
					self.psd = str(p)
					cnt += 1

				if cnt == int(self.ATTENTION + self.MEDITATION + 1) :
					self.brain = np.append(self.brain, self.brainwave(), axis=0)
					cnt = 0

					cv2.imshow(WINDOWNAME, self.img1)
					fps = int((1 - (time.time() - self.time_brain)) * 1000) - 100
					KEY = cv2.waitKey(fps)
					if KEY == key.esc :
						self.csv()
						self.finish()

					now_time = time.time()
					if now_time - start_time >= 10 * 60 :		# 10分経過したらバックアップ
						self.csv(name="brain_"+str(csv_flag))
						start_time = now_time
						csv_flag += 1

					if now_time - start_time > 10 :
						self.csv()
						self.finish()
	
if __name__ == "__main__" :
	# portを$ls /dev/tty.*で確認しておく
	mind = Mind('/dev/tty.MindWaveMobile-DevA', attention=True, meditation=True)
	mind.main()
