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
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0

    for i in range(0,500):
        x_out = read(2)
        y_out = read(4)
        z_out = read(6)
        
        
        if x_out < minx:
            minx=x_out
        
        if y_out < miny:
            miny=y_out
        
        if x_out > maxx:
            maxx=x_out
        
        if y_out > maxy:
            maxy=y_out

        time.sleep(0.1)

    print("minx: ", minx)
    print("miny: ", miny)
    print("maxx: ", maxx)
    print("maxy: ", maxy)
    print("x offset: ", (maxx + minx) / 2)
    print("y offset: ", (maxy + miny) / 2)


except:
    pass
