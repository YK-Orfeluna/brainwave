import thinkgear

PORT = '/dev/tty.MindWaveMobile-DevA'
th = thinkgear.ThinkGearProtocol(PORT)
think = th.get_packets()
print think
th.serial.close()
th.io.close()
print th.serial
exit()
for packets in think:
    for p in packets:
        if isinstance(p, thinkgear.ThinkGearRawWaveData):
            continue
        print p