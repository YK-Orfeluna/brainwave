# -*- coding: utf-8 -*
"""
=========================================================
                    BrainWave                        
=========================================================
This system is developed by Python 2.7.12 & Numpy1.1.2 & Opencv 2.4.13 & thinkgear0.2.
(c) 2016 Yuki Kitagishi
"""

#動作チェックをする

import time, sys
import thinkgear		# Pyserialが必要
import numpy as np
import cv2

class Mind() :
	def __init__(self) :
		self.img1 = np.zeros([500, 500, 1])
		self.windowname = "MindWave"
		self.brain = np.zeros([1, 12],dtype=np.float64)

	def make_image(self) :
		cv2.putText(self.img1, self.windowname, (150, 100), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		cv2.putText(self.img1, "Push 'Enter': Flag ON / OFF", (10, 200), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		cv2.putText(self.img1, "Push 'esc': Save CSV & Exit", (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		self.img2 = self.img1.copy()
		cv2.putText(self.img1, "flag: -1", (10, 400), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)
		cv2.putText(self.img2, "flag: 1", (10, 400), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.CV_AA)

	def set(self) :
		PORT = '/dev/tty.MindWaveMobile-DevA'	# portを$ls /dev/tty.*で確認しておく
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
				s.zfill(2)
			out += s
		return s

	def brainwave(self, p) :
		str_1 = "ASIC EEG Power: EEGPowerData("
		str_2 = ")"
		str_3 = ", "
		name = np.array(["delta=", "theta=", "lowalpha=", "highalpha=", "lowbeta=", "highbeta=", "lowgamma=", "midgamma="])

		p = str(p)							# pをstrに変換
		p = p.lstrip(str_1)			# pから余分な文字を取り除く
		p = p.rstrip(str_2)
		p = p.split(str_3)				# pを", "で区切ってlist形式に

		self.time_brain = time.time()
		result = [self.flag, self.nowtime(), time.time(), self.time_brain - self.start]
		for x, i in enumerate(p) :
			out = i.lstrip(name[x])
			result.append(out)
	
		out = np.array([result], dtype=np.float64)
		print(out)
		return out

	def csv(self) :							# CSV形式で保存
		file = str(self.nowtime())
		np.savetxt("brainwave_" + file + ".csv", self.brain[1:], delimiter=",")
		print("Flag, TimeStamp, Unixtime, TimePassed, Delta, Theta, Low_Alfa, High_Alfa, Low_Beta, High_Beta, Low_Gamma, Mid_Gamma")

	def finish(self) :						# 終了処理
		cv2.destroyAllWindows()
		self.th.io.close()
		self.th.serial.close()
		sys.exit()

	def main(self) :
		self.flag = -1
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
				if flag == -1 :
					cv2.imshow(self.windowname, self.img1)
				else :
					cv2.imshow(self.windowname, self.img2)
				fps = int((1 - (time.time() - self.time_brain)) * 1000) - 100
				key = cv2.waitKey(fps)
				if key == 27 :											# push "esc"
					self.csv()
					self.finish()
				elif key == 13 :										# push "enter/return"
					self.flag *= -1
					print("Change Flag to %d" %self.flag)

	
if __name__ == "__main__" :
	mind = Mind()
	mind.main()
