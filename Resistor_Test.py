#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

channel_no = 0
Read_input = 1
time_passed = 0
total_voltage = 0
voltage_list = []

while Read_input:

	# Add total time that program is outputting data
	time_passed = time_passed + .25

        # read the analog pin
        voltage = readadc(channel_no, SPICLK, SPIMOSI, SPIMISO, SPICS)

	#print voltage and voltage number
        if DEBUG:
		set_voltage = (voltage * 3.323) / 1023
                print "voltage:", set_voltage, " voltage no:", voltage

	# start summing voltage after 2 seconds has passed
	if time_passed > 2:
		total_voltage = total_voltage + voltage
		voltage_list.append(voltage)
		
	# print average voltage and voltage number and end loop
	if time_passed >= 12:
		avg_volt_no = float(total_voltage) / float(40)
#		avg_volt = (avg_volt_no * 3.323) / 1023
		max_volt = max(voltage_list)
		min_volt = min(voltage_list)
#		print "\n", "Avg voltage:", avg_volt,
		print "\n", "Avg voltage no:", avg_volt_no, " Min no:", min_volt, " Max no:", max_volt, "\n" 
		Read_input = 0

	#Wait time between voltage readings
	time.sleep(0.25)
