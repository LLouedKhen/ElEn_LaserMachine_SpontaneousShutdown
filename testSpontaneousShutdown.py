# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:23:31 2020
The El En laser pain machine spontaneously turns off after a while when no command to 
send pulse is fired. This problem is particularly pernicious in that the manual states that 
the diode turns off after " a few minutes", which hampers software workarounds. Here, I attempt
to measure what a " few minutes" actually means. 
@author: louedkhe
"""
import sys 
sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts')
sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\Laser')


import os
import glob
import numpy as np
import re
import numpy.matlib
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
from psychopy import visual, core, event, sound, logging #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import serial as serial
import time
from random import randint
import numpy as np
from datetime import datetime
from serial_ports import serial_ports
import winsound


from FireLaser import FireLaser
from LaserPainFunOpen import LaserPainFunOpen
from LaserPainFunClose import LaserPainFunClose

Times = np.zeros([5,3])

thisPort = serial_ports()

ser = serial.Serial(thisPort[0])  # open first serial port
print(ser.name)       # check which port was really used
ser.baudrate = 9600 #set baudrate to 9600 as in Manual p.47
ser.flush()

    #Now for some translating into uint8
    #Laser off, L000
L0 = [204, 76, 48, 48, 48, 185]
    #Diode off, H000
D0 = [204, 72, 48, 48, 48, 185]
    #Operate off, O000
O0 = [204, 79, 48, 48, 48, 185]
    
for i in range(0,5):
    #Type 0 when asked for serial connection - the connection should already be open
    timesLaserOn, LaserFootPulse, LaserFootSpotsize, LaserFootPulseCode, LaserFootSpotsizeCode, ser= LaserPainFunOpen(ser)
    Times[i,0]=time.time()
    resp = []
    while b'\xccL000\xb9' not in resp:
        resp = ser.read(6)
        if b'\xccL000\xb9' in resp:
                print(('\n Turned off.'))
                winsound.Beep(1000, 100)
                Times[i,1] = time.time() 
                Times[i,2] = Times[i,1] - Times[i,0] 
  

Times = pd.DataFrame(Times)

Times.to_csv('ShutdownDuration.csv')