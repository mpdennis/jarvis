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
#	print("%.6f" % volts), "Volts"
	temp = volts/.03
	print ("%.1f" % temp), "degrees Celsius"
	time.sleep(.1)

