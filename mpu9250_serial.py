#!/usr/bin/env python
import sys

import serial
import signal
import io

ser = serial.Serial()


def mcu_serial_start(port_name = 'COM6', baudrate = 115200):
	print("Opening port: " + port_name + " baudrate: " + str(baudrate))
	ser.baudrate = baudrate
	ser.port = port_name
	
	signal.signal(signal.SIGINT, signal_handler)

	ser.open()
	return ser.is_open

def mcu_serial_stop():
	if ser.is_open:
		ser.close()


def mcu_serial_get_data():
	b = ser.readline()
	str_rn = b.decode()
	string = str_rn.rstrip()
	string_list = string.split(",") 
	return float(string_list[0]), float(string_list[1]), float(string_list[2])


def signal_handler(sig, frame):
	print('Serial close')
	ser.close()
	
	# sys.exit(0)
