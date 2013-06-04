#!/usr/bin/env python

import serial
import time

# /dev/ttyACM0 = Arduino Uno on Linux
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2) #waiting the initialization...

arduino.write('H') #turns LED *on*
time.sleep(3) #zzz

arduino.write('L') #turns LED *off*
time.sleep(3) #zzz

arduino.close() #let's say goodbye
