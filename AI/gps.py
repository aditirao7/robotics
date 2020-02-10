import serial
import time

ser = serial.Serial("/dev/ttyUSB0")

while True:
    try:
        time.sleep(0.01)
        ser_bytes = ser.readline()
        decoded=ser_bytes.decode()
        if decoded.startswith('$GPGGA'):
          list1=decoded.split(',')
          print('Latitude:', list1[3])
          print('Longitude:', list1[5])
          print('\n')
    except KeyboardInterrupt:
        break
