#!/usr/local/bin/python2

import time
import smbus
import math
from Adafruit_ADS1x15 import ADS1x15

#Initializes chip, gain, and samples per second
ADS1115 = 0x1
gain = 4096
sps = 640

#Takes in the ID voltage and the data voltage from one set of pins
#Determines ID and then output algorithm corresponding to sensor
def ID(ID,output):
	if(ID <= 0.0735):
	# ID = 1, UV Sensor
		UV = output * 12.49 - 12.49
		print ("%.4f" % UV), "mW/m^2"
        elif(0.0735 < ID <= 0.2535):
	# ID = 2, Surface Temperature Sensor
		temp = (output - .5) / .01
		print ("%.1f" % temp), "degrees Celsius"
                return 2
        elif(0.2535 < ID <= 0.455):
	# ID = 3, Vibration Sensor
		print("%.4f" % output), "Vibration Voltage"
                return 3
        elif(0.455 < ID <= .582):
	# ID = 4, Motion Sensor
		if output > 3:
               		print "Motion Detected"
	        else:
        	        print "No Motion Detected"
                return 4
        elif(0.582 < ID <= 0.737):
	# ID = 5, Magnetic Door Sensor
		if output <= 0:
            	    	print "Magnetic Field Detected"
        	else:
                	print "No Magentic Field Detected"
                return 5
        elif(0.737 < ID <= 0.95):
	# ID = 6, Noise Voltage
		
                return 6
        elif(0.95 < ID <= 1.14):
                return 7
        elif(1.14 < ID <= 1.29):
                return 8
        elif(1.29 < ID <= 1.40):
                return 9
        elif(1.40 < ID <= 1.625):
                return 10
        elif(1.625 < ID <= 1.795):
                return 11
        elif(1.795 < ID <= 1.96):
                return 12
        elif(1.96 < ID <= 2.15):
                return 13
        elif(2.15 < ID <= 2.325):
                return 14
        elif(2.325 < ID <= 2.505):
                return 15
        elif(2.505 < ID <= 2.654):
                return 16
	elif(2.654 < ID <= 2.8725):
                return 17
        elif(2.8745 < ID <= 3.0635):
                return 18
        elif(3.0645 < ID <= 3.23):
                return 19
        elif(ID > 3.23):
                return 20

#Reads in two bytes of data from data registers in BMP180 and converts to integer
def BMP180_Read(bus, addr, reg, val):
        bus.write_byte_data(addr, reg, val)
        time.sleep(.005)
        msb = bus.read_byte_data(addr, 0xF6)
        lsb = bus.read_byte_data(addr, 0xF7)
        data = msb*256+lsb
        return data

#Reads in integer values for temperature and air pressure from BMP180
#Converts integer values into respective units
def BMP180_Convert(temp_data, pressure_data):
	#BMP180 calibration data
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

	#Calculate true temp
        X1 = (float(temp_data) - float(AC6)) *float(AC5)/(2**15)
        X2 = float(MC) * (2**11) / (float(X1) + float(MD))
        B5 = float(X1) + float(X2)
        T = (float(B5)+8)/(2**4)
        T=int(T)
        T=float(T)/10
	print T, "degrees C"
	
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
	print p, "Pa"
	
	return T,p

#Reads in values from data registers from TSL2561
#Converts data into lux
def TSL2561(addr):
	low0 = 0x8C
	high0 = 0x8D
	low1 = 0x8E
	high1 = 0x8F	
	
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
	print lux, "lux"
	return lux

#Initializes all 8 data pins on sensor board
analog0 = ADS1x15(0x48, ic=ADS1115)
analog1 = ADS1x15(0x48, ic=ADS1115)
analog2 = ADS1x15(0x49, ic=ADS1115)
analog3 = ADS1x15(0x49, ic=ADS1115)
analog4 = ADS1x15(0x4a, ic=ADS1115)
analog5 = ADS1x15(0x4a, ic=ADS1115)
analog6 = ADS1x15(0x4b, ic=ADS1115)
analog7 = ADS1x15(0x4b, ic=ADS1115)

#Initializes all 8 ID pins on sensor board
ID0 = ADS1x15(0x48, ic=ADS1115)
ID1 = ADS1x15(0x48, ic=ADS1115)
ID2 = ADS1x15(0x49, ic=ADS1115)
ID3 = ADS1x15(0x49, ic=ADS1115)
ID4 = ADS1x15(0x4a, ic=ADS1115)
ID5 = ADS1x15(0x4a, ic=ADS1115)
ID6 = ADS1x15(0x4b, ic=ADS1115)
ID7 = ADS1x15(0x4b, ic=ADS1115)

#Sets i2c bus line to Raspberry Pi Revision 2
bus = smbus.SMBus(1)

#BMP180 hex values
BMP180_addr = 0x77
control_reg = 0xF4
temp_value = 0x2E
press_value = 0x34

#TSL2561 hex values
TSL2561_addr = 0x39
startaddr = 0x80
startval = 0x03

while True:
	#Starts data collection for TSL2561
	try:
		bus.write_byte_data(TSL2561_addr, startaddr, startval)
	except:
		pass

	#Starts data collection for BMP180 and reads data for temperature and air pressure
        try:
		temp_data = BMP180_Read(bus, BMP180_addr, control_reg, temp_value)
        	pressure_data = BMP180_Read(bus, BMP180_addr, control_reg, press_value)

		#Get converted temperature and pressure 
		BMP180_Temp,BMP180_Pressure = BMP180_Convert(temp_data,pressure_data)
	except:      
 		pass
	
	#Get converted lux
	try:
		TSL2561_lux = TSL2561(TSL2561_addr)
	except:
		pass

	#Collecting and converting data from analog pinset 1
	x48_0 = analog0.readADCSingleEnded(0, gain, sps) / 1000
	x48_1 = ID0.readADCSingleEnded(1, gain, sps) / 1000
	ID(x48_1,x48_0)

	#Collecting and converting data from analog pinset 2
	x48_3 = analog1.readADCSingleEnded(3, gain, sps) / 1000
        x48_2 = ID1.readADCSingleEnded(2, gain, sps) / 1000
        ID(x48_2,x48_3)

	#Collecting and converting data from analog pinset 3
#	x49_0 = analog2.readADCSingleEnded(0, gain, sps) / 1000
 #       x49_1 = ID2.readADCSingleEnded(1, gain, sps) / 1000
  #      ID(x49_1,x49_0)

	#Collecting and converting data from analog pinset 4
#	x49_2 = analog3.readADCSingleEnded(2, gain, sps) / 1000
 #       x49_3 = ID3.readADCSingleEnded(3, gain, sps) / 1000
  #      ID(x49_3,x49_2)

	#Collecting and converting data from analog pinset 5
	x4a_0 = analog4.readADCSingleEnded(0, gain, sps) / 1000
        x4a_1 = ID4.readADCSingleEnded(1, gain, sps) / 1000
        ID(x4a_1,x4a_0)

	#Collecting and converting data from analog pinset 6
	x4a_3 = analog5.readADCSingleEnded(3, gain, sps) / 1000
        x4a_2 = ID5.readADCSingleEnded(2, gain, sps) / 1000
        ID(x4a_2,x4a_3)

	#Collecting and converting data from analog pinset 7
	x4b_1 = analog6.readADCSingleEnded(1, gain, sps) / 1000
        x4b_0 = ID6.readADCSingleEnded(0, gain, sps) / 1000
        ID(x4b_0,x4b_1)

	#Collecting and converting data from analog pinset 8
	x4b_2 = analog7.readADCSingleEnded(2, gain, sps) / 1000
        x4b_3 = ID7.readADCSingleEnded(3, gain, sps) / 1000
        ID(x4b_3,x4b_2)

	print "--------------------------------------------"

	time.sleep(.5)
