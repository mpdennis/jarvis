#!/usr/local/bin/python2

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN)

while True:

	input_value = GPIO.input(12)
	print input_value
	time.sleep(.5)
