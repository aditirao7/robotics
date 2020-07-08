import serial
import time
import numpy as np
from math import *
import smbus
import time

bus = smbus.SMBus(1)
ser = serial.Serial("/dev/ttyUSB0")

dev_add = 0x1E
reg_A = 0x00
reg_B = 0x01
mode_reg = 0x02

bus.write_byte_data(dev_add, reg_A, 0x70)
bus.write_byte_data(dev_add, reg_B, 0xA0)
bus.write_byte_data(dev_add, mode_reg, 0x00)

declination = -1.53589
pi =3.14159265359
lat2=1334.786166
lon2=7479.216999

time.sleep(0.6)

def read(addr):
    data=bus.read_i2c_block_data(dev_add, reg_B, 8)
    high = data[addr]
    low = data[addr+1]

        #concatenate higher and lower value
    value = ((high << 8) | low)

        #to get signed value from module
    if(value > 32768):
        value = value - 65536
    return value

def gps():
    time.sleep(0.01)
    ser_bytes = ser.readline()
    decoded=ser_bytes.decode()
    if decoded.startswith('$GPGGA'):
        list1=decoded.split(',')
        latlon=np.array([list1[2], list1[4]])
        return

def calcBearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)
    return atan2(y, x)

try:
        while 1:

            x = read(2)
            y = read(4)
            z = read(6)
            print(x,y,z)

            heading = math.atan2(y, x) + declination

            #Due to declination check for >360 degree
            if(heading > 2*pi):
                   heading = heading - 2*pi

            #check for sign
            if(heading < 0):
                    heading = heading + 2*pi

            #convert into angle
            heading_angle = int(heading * 180/pi)

            #print ("Heading Angle = %d°" %heading_angle)

            current = gps()
            lat1 = current[0]
            lon1 = current[1]

            Bearing = calcBearing(lat1, lon1, lat2, lon2)
            Bearing = degrees(Bearing)

            angle=Heading-Bearing
            print(angle)
except:
    pass
