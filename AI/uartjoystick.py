import pygame
import serial

ser = serial.Serial('/dev/ttyUSB0')
def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

pygame.init()
print ("Joysticks: ", pygame.joystick.get_count())
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        x=-1*my_joystick.get_axis(0)
        y=my_joystick.get_axis(1)
        x=(map(x, -1, 1, -1023, 1023))
        y=map(y, -1, 1, -1023, 1023)
        clock.tick(100)
        ledR=0
        ledL=0
        if (y > 10):
            ledR = map(y, 10, 1023, 0, 255)
            ledL = map(y, 10, 1023, 0, 255)
        elif (y < -10):
            ledR = map(y, -10, -1023, 0, -255)
            ledL = map(y, -10, -1023, 0, -255)
        else:
            ledR = 0
            ledL = 0
        if (x > 10):
            X = map(x, 10, 1023, 0, 255);
            ledR = ledR - X;
            ledL = ledL + X;
            if (ledL > 255):
                ledL = 255
            if (ledR < -255):
                ledR = -255
        elif (x < -10):
            X = map(x, -10, -1023, 0, 255);
            ledR = ledR + X;
            ledL = ledL - X;
            if (ledR > 255):
                ledR = 255
            if (ledL < -255):
                ledL = -255

        print(ledL, '\t', ledR)
        line = str(ledR)
        line = line.encode()
        ser.write(line)  # write a string

pygame.quit ()
                                     
