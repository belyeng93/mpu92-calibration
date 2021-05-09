#!/usr/bin/env python
import sys

import serial
import signal
import io

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM6'



def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	ser.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ser.open()

print(ser.is_open)

while ser.is_open:
	b = ser.readline()
	str_rn = b.decode()
	string = str_rn.rstrip()
	string_list = string.split(",") 
	print(string_list)

ser.close()