#!/usr/local/bin/python2

import time
import smbus
from bitstring import BitArray

def sCalibrate(bus, addr, msb, lsb):
	M = bus.read_byte_data(addr, msb)
	N = bus.read_byte_data(addr, lsb)
	comb = M*256+N
	b = BitArray(hex(comb))
	signed_int =  b.int
	return signed_int

def uCalibrate(bus, addr, msb, lsb):
        M = bus.read_byte_data(addr, msb)
        N = bus.read_byte_data(addr, lsb)
        comb = M*256+N
        b = BitArray(hex(comb))
        signed_int =  b.uint
        return signed_int

def Read(bus, addr, reg, val):
	bus.write_byte_data(addr, reg, val)
        time.sleep(.005)
        msb = bus.read_byte_data(addr, 0xF6)
        lsb = bus.read_byte_data(addr, 0xF7)
	data = msb*256+lsb
	return data

bus = smbus.SMBus(1)
addr = 0x77
control_reg = 0xF4
temp_value = 0x2E
press_value = 0x34

#Calibration data
AC1 = 408
AC2 = -72
AC3 = -14383
AC4 = 32741
AC5 = 32757
AC6 = 23153
B1 = 6190
B2 = 4
MB = -32768
MC = -8711
MD = 2868
#AC1 = sCalibrate(bus, addr, 0xAA, 0xAB)
#AC2 = sCalibrate(bus, addr, 0xAC, 0xAD)
#AC3 = sCalibrate(bus, addr, 0xAE, 0xAF)
#AC4 = uCalibrate(bus, addr, 0xB0, 0xB1)
#AC5 = uCalibrate(bus, addr, 0xB2, 0xB3)
#AC6 = uCalibrate(bus, addr, 0xB4, 0xB5)
#B1 = sCalibrate(bus, addr, 0xB6, 0xB7)
#B2 = sCalibrate(bus, addr, 0xB8, 0xB9)
#MB = sCalibrate(bus, addr, 0xBA, 0xBB)
#MC = sCalibrate(bus, addr, 0xBC, 0xBD)
#MD = sCalibrate(bus, addr, 0xBE, 0xBF)

print AC1, AC2, AC3, AC4, AC5, AC6, B1, B2, MB, MC, MD

while True:
	#Read data for temp and pressure
	temp_data = Read(bus, addr, control_reg, temp_value)
	pressure_data = Read(bus, addr, control_reg, press_value)

	#Calculate true temp
	X1 = (float(temp_data) - float(AC6)) *float(AC5)/(2**15)
	X2 = float(MC) * (2**11) / (float(X1) + float(MD))
	B5 = float(X1) + float(X2)
	T = (float(B5)+8)/(2**4)
	T=int(T)
	T=float(T)/10
	print T,"degrees Celsius"

	#Calculate true pressure
	B6 = float(B5) - 4000
	X1 = (float(B2)*(float(B6)*float(B6)/(2**12)))/(2**11)
	X2 = float(AC2) * float(B6)/(2**11)
	X3 = float(X1) + float(X2)
	B3 = (((float(AC1)*4+float(X3))*1)+2)/4
	X1 = float(AC3) * float(B6)/(2**11)
	X2 = (float(B1) * (float(B6)*float(B6)/(2**12)))/(2**16)
	X3 = ((float(X1)+float(X2))+2)/4
	B4 = float(AC4)*(float(X3) +32768)/(2**15)
	B7 = (float(pressure_data) - float(B3))*(50000)
	if B7 < 0x80000000:
		p = (float(B7) * 2)/float(B4)
	else:
		p = (float(B7)/float(B4))*2
	X1 = (float(p)/(2**8))*(float(p)/(2**8))
	X1 = (float(X1) * 3038) / (2**16)
	X2 = (-7357*float(p))/(2**16)
	p = float(p) + (float(X1)+float(X2)+3791)/(2**4)
	p = int(p) - 21000
	print p,"Pa"
	time.sleep(.5)
