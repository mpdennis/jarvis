#!/usr/local/bin/python2

import time
import smbus

bus = smbus.SMBus(1)

addr = 0x39
low0 = 0x8C
high0 = 0x8D
low1 = 0x8E
high1 = 0x8F
startaddr = 0x80
startval = 0x03

bus.write_byte_data(addr, startaddr, startval)

while True:
	lux = 0
	low0_data = bus.read_byte_data(addr,low0)
	high0_data = bus.read_byte_data(addr,high0)
	CH0 = 256 * high0_data + low0_data
	if CH0 != 0:
		low1_data = bus.read_byte_data(addr, low1)
		high1_data = bus.read_byte_data(addr, high1)
		CH1 = 256 * high1_data + low1_data
		data = CH1/float(CH0)

		if(0 < data <= 0.52):
			lux = 0.0315 * CH0 - 0.0593 * CH0 * (data**1.4)
		elif(0.52 < data <= 0.65):
			lux = 0.0229 * CH0 - 0.0291 * CH1
		elif(0.65 < data <= 0.80):
			lux = 0.0157 * CH0 - 0.0180 * CH1
		elif(0.80 < data <= 1.30):
			lux = 0.00338 * CH0 - 0.00260 * CH1
		elif(data > 1.30):
			lux = 0

	print(lux)
	time.sleep(1)
