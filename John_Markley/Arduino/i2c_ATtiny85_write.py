#!/usr/bin/python

import smbus
import time
bus = smbus.SMBus(1)
device_address = 0x30 #address space 28
device_register = 0x00 #ATtiny does not read the register leave this zero
device_data = 0x03 #Output 3

bus.write_byte_data(device_address, device_register, device_data)
time.sleep(1)
print ("Output 1 has switched state.")
