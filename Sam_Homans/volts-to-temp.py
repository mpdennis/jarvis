import time
import smbus
import math
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x1

gain = 6144

sps = 860

adc = ADS1x15(ic=ADS1115)

while True:
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000
	Temp = (volts - .5)/.01 
	print ("%.4f" % Temp), "°C"
	time.sleep(.1)
