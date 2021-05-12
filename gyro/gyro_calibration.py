######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag)
# and solves for calibration coefficients for the
# gyroscope
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
            if(mpu9250_serial.mcu_serial_start(port_name = "/dev/ttyUSB0")):
                start_bool = True
                break

        except:
            continue

import numpy as np
import csv,datetime
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

time.sleep(2) # wait for MPU to load and settle
# 
#####################################
# Gyro calibration (Steady)
#####################################
#
def get_gyro():
    _,_,_,wx,wy,wz = mpu6050_conv() # read and convert gyro data
    return wx,wy,wz
def gyro_cal():
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    mpu_array = [] # imu array for gyro vals
    gyro_offsets = [0.0,0.0,0.0] # gyro offset vector
    while True:
        try:
            if not USING_SERIAL_DATA_FROM_MCU:
                wx,wy,wz = get_gyro() # get gyro vals
            else:
                wx,wy,wz = mpu9250_serial.mcu_serial_get_data()
        except:
            continue

        mpu_array.append([wx,wy,wz]) # gyro vector append
        print(len(mpu_array))
        if np.shape(mpu_array)[0]==cal_size:
            for qq in range(0,3):
                gyro_offsets[qq] = np.mean(np.array(mpu_array)[:,qq]) # calc gyro offsets
            break
    print('Gyro Calibration Complete')
    return gyro_offsets # return gyro coeff offsets


if __name__ == '__main__':
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        #
        ###################################
        # Gyroscope Offset Calculation
        ###################################
        #
        gyro_labels = ['w_x','w_y','w_z'] # gyro labels for plots
        # cal_size = 500 # points to use for calibration
        cal_size = 10 # points to use for calibration
        gyro_offsets = gyro_cal() # calculate gyro offsets
        #
        ###################################
        # Record new data 
        ###################################
        #
        input("Press Enter and Rotate Gyro 360 degrees")
        print("Recording Data...")
        record_time = 5 # how long to record
        data,t_vec = [],[]
        t0 = time.time()
        while time.time()-t0 < record_time:
            if not USING_SERIAL_DATA_FROM_MCU:
                data.append(get_gyro())
            else:
                data.append(np.array(mpu9250_serial.mcu_serial_get_data()))
            t_vec.append(time.time()-t0)
        samp_rate = np.shape(data)[0]/(t_vec[-1]-t_vec[0]) # sample rate
        print("Stopped Recording\nSample Rate: {0:2.0f} Hz".format(samp_rate))

        mpu9250_serial.mcu_serial_stop()

        data = np.array(data)

        #
        ###################################
        # Plot with and without offsets
        ###################################
        #
        plt.style.use('ggplot')
        fig,axs = plt.subplots(2,1,figsize=(12,9))
        for ii in range(0,3):
            axs[0].plot(data[:,ii],
                        label='${}$, Uncalibrated'.format(gyro_labels[ii]))
            axs[1].plot(data[:,ii]-gyro_offsets[ii],
                        label='${}$, Calibrated'.format(gyro_labels[ii]))
        axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
        axs[0].set_ylabel('$w_{x,y,z}$ [$^{\circ}/s$]',fontsize=18)
        axs[1].set_ylabel('$w_{x,y,z}$ [$^{\circ}/s$]',fontsize=18)
        axs[1].set_xlabel('Sample',fontsize=18)
        axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
        axs[0].set_title('Gyroscope Calibration Offset Correction',fontsize=22)
        fig.savefig('gyro_calibration_output.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
        fig.show()
        plt.show()
