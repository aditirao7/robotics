import serial
import pickle
import time
ser = serial.Serial('/dev/ttyUSB0')
line = "hello"
line= line.encode()
while 1:
    ser.write(line)     # write a string
