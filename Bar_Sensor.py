#!/usr/local/bin/python2

import time
import smbus
from bitstring import BitArray

bus = smbus.SMBus(1)

addr = 0x77
startaddr = 0x80
temp_addr = 0x00
control_addr = 0xF4

while True:
	AC1m = bus.read_byte_data(addr, 0xAA)
	AC1l = bus.read_byte_data(addr, 0xAB)
	print "AC1:", AC1m *256 + AC1l
	AC2m = bus.read_byte_data(addr, 0xAC)
        AC2l = bus.read_byte_data(addr, 0xAD)
	AC2 = AC2m*256+AC2l
	b = BitArray(bin(AC2))
        print "AC2: ", b.int, AC2
	bus.write_byte_data(addr, 0xF4, 0x2E)
	time.sleep(.5)
	msbdata = bus.read_byte_data(addr, 0xF6)
	lsbdata = bus.read_byte_data(addr, 0xF7)
	#print msbdata*256 + lsbdata
