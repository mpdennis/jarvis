import time
import smbus
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x01

gain = 4096

sps = 250

adc = ADS1x15(ic=ADS1115)


while True:
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000

	print("%.6f" % volts)
	time.sleep(1)
