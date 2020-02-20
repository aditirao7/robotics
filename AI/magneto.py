import smbus
import time
import math
bus = smbus.SMBus(1)

dev_add = 0x1E
reg_A = 0x00
reg_B = 0x01
mode_reg = 0x02

bus.write_byte_data(dev_add, reg_A, 0x70)
bus.write_byte_data(dev_add, reg_B, 0xA0)
bus.write_byte_data(dev_add, mode_reg, 0x00)

declination = -0.00669
pi =3.14159265359

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

        print ("Heading Angle = %d°" %heading_angle)
except:
    pass
                                                                                                                                                        1,12          Top
