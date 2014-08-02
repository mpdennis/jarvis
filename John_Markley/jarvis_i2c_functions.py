#!/usr/bin/env python

import time
import smbus
import math
import sys
import os.path
from jarvis_conversion import ADS1115_LM36

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x01
gain = 6144
sps = 860
adc = ADS1x15(ic=ADS1115)

# setup file output
file = open("tempoutput.txt", "w")
file.write("Type,Value,Unit,Raw\n")

loopnumber=200 # number of times to loop.
# loop data retrieval

x=0 # Initialize loop
while True:
	# Retrieve the voltage from the ADS1115 input 0
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000
	# convert the voltage to degrees
	tempc = ADS1115_LM36(volts, "C")
	# pause .1 seconds
	time.sleep(.1)
	# write the value to a file
	file.write("temp,"+("%.1f" % tempc)+",Celsius,"+("%.6f" % volts)+"\n")
###############################
##      Test the values      ##
###############################
#	# print the voltage out to the command line
#	print("%.6f" % volts), "Volts"
# 	# print the temperture out to the command line in degrees Fahrenheit
#	print ("%.1f" % tempf), "degrees Fahrenheit"
#	# print the temperture out to the command line in degrees Celsius
#	print ("%.1f" % tempc), "degrees Celsius"
	
	# Increment loop by 1
	x += 1  
	if x == loopnumber:
		# exit loop
		break 
# close the file
file.close()
