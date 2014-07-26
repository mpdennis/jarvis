import time
import smbus
import math
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x01

gain = 6144

sps = 860

adc = ADS1x15(ic=ADS1115)
file = open("tempoutput.txt", "w")
file.write("Type,Value,Unit,Raw\n")
x=0
while True:
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000
#	print("%.6f" % volts), "Volts"
	tempc = volts/.03
	tempf = (tempc*9/5)+32
	print ("%.1f" % tempc), "degrees Celsius"
#	print ("%.1f" % tempf), "degrees Fahrenheit"
	time.sleep(.1)
	file.write("temp,"+("%.1f" % tempc)+",Celsius,"+("%.6f" % volts)+"\n")
	x += 1
	if x == 200:
		break
file.close()
