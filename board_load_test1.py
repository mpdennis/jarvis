#!/usr/local/bin/python2

import time
import smbus
from bitstring import BitArray
import math
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x1
gain = 6144
sps = 860

adc = ADS1x15(0x4a, ic=ADS1115)
adc1 = ADS1x15(0x4b, ic=ADS1115)
adc2 = ADS1x15(0x48, ic=ADS1115)
adc3 = ADS1x15(0x4a, ic=ADS1115)
adc4 = ADS1x15(0x4b, ic=ADS1115)
adc5 = ADS1x15(0x49, ic=ADS1115)
adc6 = ADS1x15(0x49, ic=ADS1115)
adc7 = ADS1x15(0x48, ic=ADS1115)

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
bar_addr = 0x77
control_reg = 0xF4
temp_value = 0x2E
press_value = 0x34

addr = 0x39
low0 = 0x8C
high0 = 0x8D
low1 = 0x8E
high1 = 0x8F
startaddr = 0x80
startval = 0x03

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

bus.write_byte_data(addr, startaddr, startval)

while True:
        #Read data for temp and pressure
        temp_data = Read(bus, bar_addr, control_reg, temp_value)
        pressure_data = Read(bus, bar_addr, control_reg, press_value)

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

        print lux, "Lux"

	volts = adc1.readADCSingleEnded(0, gain, sps) / 1000
        UV = volts * 12.49 -12.49
        print ("%.4f" % UV), "mW/m^2"

	volts1 = adc.readADCSingleEnded(0, gain, sps) / 1000
        print("%.4f" % volts1), "Motion"

	volts2 = adc2.readADCSingleEnded(3, gain, sps) / 1000
        print("%.4f" % volts2), "Noise Voltage"

	volts3 = adc3.readADCSingleEnded(3, gain, sps) / 1000
        print("%.4f" % volts3), "Vibration Voltage 4A"
        
	volts4 = adc4.readADCSingleEnded(2, gain, sps) / 1000
        print("%.4f" % volts4), "Vibration Voltage 4B"

	volts5 = adc5.readADCSingleEnded(2, gain, sps) / 1000
        temp = (volts5 - .5) / .01
        print ("%.1f" % temp), "degrees Celsius"	

	volts6 = adc6.readADCSingleEnded(0, gain, sps) / 1000
        print("%.4f" % volts6), "Magnetic Sensor Voltage"

	volts7 = adc7.readADCSingleEnded(0, gain, sps) / 1000
        print("%.4f" % volts7), "Vibration Voltage 48"

	print "---------------------------------", "\n"
	
	time.sleep(.5)

