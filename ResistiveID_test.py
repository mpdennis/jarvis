import time
import smbus
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x1

gain = 4096

sps = 860

adc = ADS1x15(0x48, ic=ADS1115)

while True:
        volts = adc.readADCSingleEnded(0, gain, sps) / 1000
	print volts
	if(volts <= 0.0735):
		print 1
	elif(0.0735 < volts <= 0.2535):
		print 2
	elif(0.2535 < volts <= 0.455):
		print 3
	elif(0.455 < volts <= .582):
		print 4
	elif(0.582 < volts <= 0.737):
		print 5
        elif(0.737 < volts <= 0.95):
		print 6
        elif(0.95 < volts <= 1.14):
		print 7
	elif(1.14 < volts <= 1.29):
		print 8
        elif(1.29 < volts <= 1.40):
		print 9
        elif(1.40 < volts <= 1.625):
		print 10
	elif(1.625 < volts <= 1.795):
		print 11
        elif(1.795 < volts <= 1.96):
		print 12
        elif(1.96 < volts <= 2.15):
		print 13
	elif(2.15 < volts <= 2.325):
		print 14
        elif(2.325 < volts <= 2.505):
		print 15
        elif(2.505 < volts <= 2.654):
		print 16
	elif(2.654 < volts <= 2.8725):
		print 17
        elif(2.8745 < volts <= 3.0635):
		print 18
        elif(3.0645 < volts <= 3.23):
		print 19
	elif(volts > 3.23):
		print 20

	time.sleep(.5)
