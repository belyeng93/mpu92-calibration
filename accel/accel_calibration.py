######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
# Serial plugin: Emanuele Belia
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag)
# and solves for calibration coefficients for the
# accelerometer
#
#
######################################################
#
# wait 5-sec for IMU to connect
USING_SERIAL_DATA_FROM_MCU = True

if USING_SERIAL_DATA_FROM_MCU:
	print("Check that in your MCU has been loaded mpu9250mag sketch")
	print("Check port default:  ttyUSB0")

import time, sys, serial, signal, os

sys.path.append("../")
t0 = time.time()
start_bool = False # if IMU start fails - stop calibration

while time.time()-t0<5:
	if not USING_SERIAL_DATA_FROM_MCU:
		try:
			from mpu9250_i2c import *
			start_bool = True
			break
		except:
			continue
	else:
		try:
			print("MCU(like arduino) serial data Enabled")
			path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			sys.path.append(path)
			import mpu9250_serial
			# if(mpu9250_serial.mcu_serial_start(port_name = "/dev/ttyUSB0")):
			# if(mpu9250_serial.mcu_serial_start(port_name = "/dev/ttyACM0")):
			start_bool = True
			break

		except:
			continue

import numpy as np
import csv,datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


time.sleep(2) # wait for MPU to load and settle
#
#####################################
# Accel Calibration (gravity)
#####################################
#
def accel_fit(x_input,m_x,b):
	return (m_x*x_input)+b # fit equation for accel calibration
#
def get_accel():
	ax,ay,az,_,_,_ = mpu6050_conv() # read and convert accel data
	return ax,ay,az

def accel_cal():
	print("-"*50)
	print("Accelerometer Calibration")
	mpu_offsets = [[],[],[]] # offset array to be printed
	axis_vec = ['z','y','x'] # axis labels
	cal_directions = ["upward","downward","perpendicular to gravity"] # direction for IMU cal
	cal_indices = [2,1,0] # axis indices
	for qq,ax_qq in enumerate(axis_vec):
		ax_offsets = [[],[],[]]
		print("-"*50)
		for direc_ii,direc in enumerate(cal_directions):
			input("-"*8+" Press Enter and Keep IMU Steady to Calibrate the Accelerometer with the -"+\
			  ax_qq+"-axis pointed "+direc)
			if not USING_SERIAL_DATA_FROM_MCU:
				[mpu6050_conv() for ii in range(0,cal_size)] # clear buffer between readings
			else:
				mpu9250_serial.mcu_serial_start(port_name = "/dev/ttyUSB0")
			mpu_array = []
			print("Empty Array " + str( len(mpu_array)))
			while len(mpu_array) < cal_size:
				print(str(len(mpu_array)) + "/" + str(cal_size) )
				try:
					if not USING_SERIAL_DATA_FROM_MCU:
						ax,ay,az = get_accel()
					else:
						ax,ay,az = mpu9250_serial.mcu_serial_get_data()
					mpu_array.append([ax,ay,az])
				except:
					continue
			ax_offsets[direc_ii] = np.array(mpu_array)[:,cal_indices[qq]] # offsets for direction
			if USING_SERIAL_DATA_FROM_MCU:
				mpu9250_serial.mcu_serial_stop()


		# Use three calibrations (+1g, -1g, 0g) for linear fit
		popts,_ = curve_fit(accel_fit,np.append(np.append(ax_offsets[0],
							ax_offsets[1]),ax_offsets[2]),
				   			np.append(np.append(1.0*np.ones(np.shape(ax_offsets[0])),
							-1.0*np.ones(np.shape(ax_offsets[1]))),
							0.0*np.ones(np.shape(ax_offsets[2]))),
							maxfev=10000)
		mpu_offsets[cal_indices[qq]] = popts # place slope and intercept in offset array
	print('Accelerometer Calibrations Complete')
	f = open("./acc_offsets.txt", "a+")
	f.write(str(mpu_offsets[0]) + "," + str(mpu_offsets[1]) + "," + str(mpu_offsets[2]) + "\n")
	f.close()
	return mpu_offsets

if __name__ == '__main__':
	if not start_bool:
		print("IMU not Started - Check Wiring and I2C")
	else:
		#
		###################################
		# Accelerometer Gravity Calibration
		###################################
		#
		accel_labels = ['a_x','a_y','a_z'] # gyro labels for plots
		cal_size = 500 # number of points to use for calibration 1000
		USE_ALREADY_EXIST_DATA = True
		if USE_ALREADY_EXIST_DATA:
			f = open("./acc_offsets.txt", "r")
			string_list = f.readlines()
			splitted = string_list[-1].split(",")
			splitted = [s.strip('\n') for s in splitted]
			splitted = [s.strip('[') for s in splitted]
			splitted = [s.strip(']') for s in splitted]

			accel_coeffs = [np.array([float(splitted[0].split(" ")[0]), float(splitted[0].split(" ")[1])]), 
							np.array([float(splitted[1].split(" ")[0]), float(splitted[1].split(" ")[1])]), 
							np.array([float(splitted[2].split(" ")[0]), float(splitted[2].split(" ")[1])])]
		else:
			accel_coeffs = accel_cal() # grab accel coefficients
		print(accel_coeffs)
		# [array([0.02735479, 0.00491383]), array([0.00157824, 0.0001672 ]), array([0.00673295, 0.00016298])]
		#
		###################################
		# Record new data
		###################################
		#
		print("-"*50)
		print("Recording Data...")
		data = []
		if not USING_SERIAL_DATA_FROM_MCU:
			[mpu6050_conv() for ii in range(0,cal_size)] # clear buffer between readings
		else:
			mpu9250_serial.mcu_serial_start(port_name = "/dev/ttyUSB0")
		while len(data) < cal_size:
			print(str(len(data)) + "/" + str(cal_size) )
			try:
				if not USING_SERIAL_DATA_FROM_MCU:
					data.append(np.array(get_accel()))
				else:
					# data.append(np.array(mpu9250_serial.mcu_serial_get_data()))
					data.append((mpu9250_serial.mcu_serial_get_data()))
			except:
				continue
		data = np.array(data)
		mpu9250_serial.mcu_serial_stop()
		print(accel_coeffs)


		#
		###################################
		# Plot with and without offsets
		###################################
		#
		plt.style.use('ggplot')
		fig,axs = plt.subplots(2,1,figsize=(12,9))
		for ii in range(0,3):
			axs[0].plot(data[:,ii],
						label='${}$, Uncalibrated'.format(accel_labels[ii]))

			axs[1].plot(accel_fit(data[:,ii],*accel_coeffs[ii]),
						label='${}$, Calibrated'.format(accel_labels[ii]))
		axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
		axs[0].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
		axs[1].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
		axs[1].set_xlabel('Sample',fontsize=18)
		# axs[0].set_ylim([-2,2])
		axs[1].set_ylim([-2,2])
		axs[0].set_title('Accelerometer Calibration Calibration Correction',fontsize=18)
		fig.savefig('accel_calibration_output.png',dpi=300,
					bbox_inches='tight',facecolor='#FCFCFC')
		fig.show()
		plt.show()
