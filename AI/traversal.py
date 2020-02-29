import serial
import math
import smbus
import time
from haversine import haversine ,Unit
declination = -0.00669
pi = 3.14159265359

bus= smbus.SMBus(1)
ser= serial.Serial("/dev/ttyUSB0", baudrate=4800)
ser.flushInput()

dev_add = 0x1E
reg_A = 0x00
reg_B = 0x01
mode_reg = 0x02

bus.write_byte_data(dev_add, reg_A, 0x70)
bus.write_byte_data(dev_add, reg_B, 0xA0)
bus.write_byte_data(dev_add, mode_reg, 0x00)

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

lat2 = 1320.8807/100
lon2 = 7447.5185/100
pointA=(lat2,lon2)
def heading(x,y):
    heading = math.atan2(y, x) + declination

    if (heading > 2 * pi):
        heading = heading - 2 * pi

    if (heading < 0):
        heading = heading + 2 * pi

    heading_angle = int(heading * 180 / pi)
    return heading_angle

while True:
    lat1 = 0
    lon1 = 0
    ser_bytes = ser.readline()
    ser_bytes = ser.readline()
