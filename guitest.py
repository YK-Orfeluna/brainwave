# -*- coding: utf-8 -*

import sys
if sys.version_info[0] != 2 :
	exit()
import time

import Tkinter as tk
from Tkinter import *

class Application(Frame):
	def __init__(self, master=None) :
		self.loop = True

		Frame.__init__(self, master)
		self.pack()
		self.create_widgets()

	def create_widgets(self) :
		self.start = tk.Button(self)
		self.start["text"] = "Start"
		self.start["command"] = self.main

		self.start.pack({"side": "left"})


		self.button = tk.Button(self)
		self.button["text"] = "Save & Exit"
		self.button["command"] = self.loop_end

		self.button.pack({"side": "left"})

	def loop_end(self) :
		self.loop = False

	def main(self) :
		cnt = 0
		for i in range(10000) :
			cnt += 1
			print(cnt)
			time.sleep(1)
			if self.loop == False :
				break
		print("end")

if __name__ == "__main__" :
	root = tk.Tk()
	app = Application(master=root)
	#app.main()
	app.mainloop()

	# app = Application()

	# root.title(u"BrainWave Sensing")
	# root.geometry("400x300")

	# Button = tk.Button(text="Save & Exit")
	# Button.bind("<Button-1>",app.loop_end) 
	# Button.pack()

	# app.main()

	# root.mainloop()


