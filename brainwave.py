# -*- coding: utf-8 -*

import time, sys
if sys.version_info[0] == 2 :
	import thinkgear		# Pyserialが必要
else :
	exit("*This script only supports Python2.x.\nSorry, we can not support your Python.")

import numpy as np
import cv2
import pandas as pd

import key_num as key

WINDOWNAME = "MindWave"

STR_1 = "ASIC EEG Power: EEGPowerData("
STR_2 = ")"
STR_3 = ", "

NAME = np.array(["delta=", "theta=", "lowalpha=", "highalpha=", "lowbeta=", "highbeta=", "lowgamma=", "midgamma="])
LABEL = np.array(["Unix", "TimeStamp", "Delta", "Theta", "Low_Alfa", "High_Alfa", "Low_Beta", "High_Beta", "Low_Gamma", "Mid_Gamma"])

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
		if attention :	
			np.append(NAME, "attention=")
			np.append(LABEL, "Attention")

		self.meditation = meditation
		if meditation :
			np.append(NAME, "meditation=")
			np.append(LABEL, "Meditation")

		self.img1 = np.zeros([500, 500, 1])
		self.brain = np.zeros([1, LABEL.shape[0]])

		self.th = thinkgear.ThinkGearProtocol(port)
		self.th = thinkgear.ThinkGearProtocol(port)
		self.think = self.th.get_packets()
		print(self.think)		

	def brainwave(self, p) :
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
	
		out = np.array([result])
		if self.DEBUG :
			print(out)
		return out

	def csv(self, name="brain") :							# CSV形式で保存
		v = self.brain[1:]
		c = LABEL
		df = pd.DataFrame(v, columns=c)
		df.to_csv(name+".csv", index=False, encoding="utf-8")

	def finish(self) :						# 終了処理
		cv2.destroyAllWindows()
		self.th.io.close()
		self.th.serial.close()
		sys.exit()

	def main(self) :
		start_time = time.time()
		csv_flag = 1

		for packets in self.think:
			for p in packets:
				if isinstance(p, thinkgear.ThinkGearRawWaveData):		# Rawデータを取り除く
					continue
				if isinstance(p, thinkgear.ThinkGearPoorSignalData):	# Poorシグナルを取り除く	
					continue
				if self.ATTENTION :
					if isinstance(p, thinkgear.ThinkGearAttentionData):		# Attention値を取り除く
						continue
				if self.MEDITATION :
					if isinstance(p, thinkgear.ThinkGearMeditationData):	# Meditation値を取り除く
						continue
				#if isinstance(p, thinkgear.ThinkGearEEGPowerData):		# フーリエ変換されたデータを取り除く	
				#	continue

				self.brain = np.append(self.brain, self.brainwave(p), axis=0)

				cv2.imshow(WINDOWNAME, self.img1)
				fps = int((1 - (time.time() - self.time_brain)) * 1000) - 100
				KEY = cv2.waitKey(fps)
				if KEY == key.esc :
					self.csv()
					self.finish()

				now_time = time.time()
				if now_time - start_time >= 10 * 60 :
					self.csv(name="brain_"+str(csv_flag))
					start_time = now_time
					csv_flag += 1
	
if __name__ == "__main__" :
	# portを$ls /dev/tty.*で確認しておく
	mind = Mind('/dev/tty.MindWaveMobile-DevA')
	mind.main()
