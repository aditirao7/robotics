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
    decoded = ser_bytes.decode()
    if decoded.startswith('$GPGGA'):
        list1 = decoded.split(',')
        lat1 = float(list1[2])/100
        lon1 = float(list1[4]) /100
        pointB=(lat1,lon1)
        X = math.cos(lat2) * math.sin(lon2 - lon1)
        Y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
        bearing= math.atan2(X, Y)

        x = read(2)
        y = read(4)
        z = read(6)
        heading_angle=heading(x,y)
        angle=heading_angle-bearing
        print(angle)
        print("Distance:", haversine(pointA,pointB)*1000)
        if(angle>0):
                if (angle < 180):
                    print("Turn right")
                elif (angle > 180):
                    print("Turn left")
                elif (angle == 180):
                    print("Face the other way")
        if(angle<0):
                angle=abs(angle)
                if (angle > 180):
                    print("Turn right")
                elif (angle < 180):
                    print("Turn left")
                elif (angle == 180):
                    print("Face the other way")
        elif(angle == 0):
                print("Move straight")
