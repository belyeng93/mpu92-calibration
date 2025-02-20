#!/usr/bin/env python
######################################################
# Copyright (c) 2021 EmSolutions
# Author:  Emanuele Belia
######################################################
#
# This code is for handle serial communication and
# is for parse mag, gyro, acc serial sketch for your MCU
# (like Arduino)
#
######################################################
import sys

import serial
import signal
import io

ser = serial.Serial()

def mcu_serial_start(port_name = 'COM6', baudrate = 115200):
	print("Opening port: " + port_name + " baudrate: " + str(baudrate))
	ser.baudrate = baudrate
	ser.port = port_name
	ser.open()
	if ser.is_open:
		print("MPU9250 Serial Open")
	return ser.is_open

def mcu_serial_stop():
	if ser.is_open:
		print("MPU9250 Serial Close")
		ser.close()
def mcu_serial_flush():
	ser.flush()

def mcu_serial_get_data():
	b = ser.readline()
	str_rn = b.decode()
	string = str_rn.rstrip()
	string_list = string.split(",")
	# ax,ay,az,wx,wy,wz,mx,my,mz
	try:
		return float(string_list[0]), float(string_list[1]), float(string_list[2]), float(string_list[3]), float(string_list[4]), float(string_list[5]), float(string_list[6]), float(string_list[7]), float(string_list[8])
	except:
		print("err")
		return 0, 0, 0, 0, 0, 0, 0, 0, 0

if __name__ == "__main__":
	mcu_serial_start(port_name = '/dev/ttyUSB1', baudrate = 115200)
	while True:
		print(mcu_serial_get_data())
