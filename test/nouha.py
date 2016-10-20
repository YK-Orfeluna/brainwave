# -*- coding: utf-8 -*

import thinkgear

PORT = '/dev/tty.MindWaveMobile-DevA'	#　portを$ls /dev/tty.*で確認しておく
think = thinkgear.ThinkGearProtocol(PORT).get_packets()
print think

for packets in think:
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
		
		p = str(p)												# pをstrに変換
		p = p.lstrip("ASIC EEG Power: EEGPowerData(")			# pから余分な文字を取り除く
		p = p.rstrip(")")
		p = p.split(", ")										# pを", "で区切ってlist形式に

		result = []
		name = ['delta=', 'theta=', 'lowalpha=', 'highalpha=', 'lowbeta=', 'highbeta=', 'lowgamma=', 'midgamma=']
		for x, i in enumerate(p) :
			out = i.lstrip(name[x])
			result.append(out)

		print result
		
