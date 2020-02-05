import serial
import time


ser = serial.Serial('/dev/ttyS0')
ser.flushInput()

while True:
    try:
        time.sleep(0.01)
        ser_bytes = ser.read(6)
        ledL=int.from_bytes(ser_bytes[0:3], "big", signed=True)
        ledR=int.from_bytes(ser_bytes[3:6], "big", signed=True)
        print(ledL, '\t', ledR)
    except:
        print("Keyboard Interrupt")
        break
