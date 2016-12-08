# -*- coding: utf-8 -*

import time, sys
import thinkgear		# Pyserialが必要
import numpy as np
import cv2

import key_num as key

WINDOWNAME = "MindWave"
PORT = '/dev/tty.MindWaveMobile-DevA'	# PORTを$ls /dev/tty.*で確認しておく

STR_1 = "ASIC EEG Power: EEGPowerData("
STR_2 = ")"
STR_3 = ", "
NAME = np.array(["delta=", "theta=", "lowalpha=", "highalpha=", "lowbeta=", "highbeta=", "lowgamma=", "midgamma="])


class Mind() :
	def __init__(self) :
		self.img1 = np.zeros([500, 500, 1])
		self.brain = np.zeros([1, 12],dtype=np.int64)
		self.flag = -1

	def make_image(self) :
		cv2.putText(self.img1, WINDOWNAME, (150, 100), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		cv2.putText(self.img1, "Push 'Enter': Flag ON / OFF", (10, 200), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		cv2.putText(self.img1, "Push 'esc': Save CSV & Exit", (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		self.img2 = self.img1.copy()
		cv2.putText(self.img1, "flag: -1", (10, 400), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		cv2.putText(self.img2, "flag: 1", (10, 400), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)

	def set(self) :
		self.th = thinkgear.ThinkGearProtocol(PORT)
		self.think = self.th.get_packets()
		print self.think
		self.make_image()
		self.start = time.time()

	def make_zero(self, value) :
		out = str(value)
		if value < 10 :
			out = out.zfill(2)				# 桁揃え
		return out

	def nowtime(self) :
		t = time.localtime()
		stamp = [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec]
		out = ""
		for i in stamp :
			s = str(i)
			if i < 10 :
				s = "0" + s
			out += s
		return out

	def brainwave(self, p) :
		p = str(p)					# pをstrに変換
		p = p.lstrip(STR_1)			# pから余分な文字を取り除く
		p = p.rstrip(STR_2)
		p = p.split(STR_3)			# pを", "で区切ってlist形式に

		t = time.localtime()

		self.time_brain = time.time()
		result = [self.flag, t.tm_hour, t,.tm_min, t.tm_sec, self.time_brain - self.start]
		for x, i in enumerate(p) :
			out = i.lstrip(NAME[x])
			result.append(out)
	
		out = np.array([result], dtype=np.int64)
		print(out)
		return out

	def csv(self) :							# CSV形式で保存
		file = str(self.nowtime())
		np.savetxt("brainwave_" + file + ".csv", self.brain[1:], delimiter=",")
		print("Flag, Hour, Minute, Second, TimePassed, Delta, Theta, Low_Alfa, High_Alfa, Low_Beta, High_Beta, Low_Gamma, Mid_Gamma")

	def finish(self) :						# 終了処理
		cv2.destroyAllWindows()
		self.th.io.close()
		self.th.serial.close()
		sys.exit()

	def main(self) :
		self.set()

		for packets in self.think:
			for p in packets:
				if isinstance(p, thinkgear.ThinkGearRawWaveData):		# Rawデータを取り除く
					continue
				if isinstance(p, thinkgear.ThinkGearPoorSignalData):	# Poorシグナルを取り除く	
					continue
				if isinstance(p, thinkgear.ThinkGearAttentionData):		# Attention値を取り除く
					continue
				if isinstance(p, thinkgear.ThinkGearMeditationData):	# Meditation値を取り除く
					continue
				#if isinstance(p, thinkgear.ThinkGearEEGPowerData):		# フーリエ変換されたデータを取り除く	
				#	continue

				self.brain = np.append(self.brain, self.brainwave(p), axis=0)
				if self.flag == -1 :
					cv2.imshow(WINDOWNAME, self.img1)
				else :
					cv2.imshow(WINDOWNAME, self.img2)

				fps = int((1 - (time.time() - self.time_brain)) * 1000) - 100
				
				KEY = cv2.waitKey(fps)
				if KEY == key.esc :
					self.csv()
					self.finish()
				elif KEY == key.enter :
					self.flag *= -1
					print("Change Flag to %d" %self.flag)

	
if __name__ == "__main__" :
	mind = Mind()
	mind.main()
