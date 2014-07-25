import time
import smbus
import math
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x1

gain = 6144

sps = 860

adc1 = ADS1x15(0x4b, ic=ADS1115)
adc = ADS1x15(0x4a, ic=ADS1115)
#adc1 = ADS1x15(0x4b, ic=ADS1115)

while True:
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000
	volts1 = adc1.readADCSingleEnded(1, gain, sps) / 1000
	print("%.4f" % volts1), "UV Volts"
	print("%.4f" % volts), "Motion", "\n"
	time.sleep(.5)

