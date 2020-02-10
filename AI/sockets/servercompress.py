import socket
import cv2
import numpy as np
import pickle
import time

cap = cv2.VideoCapture(0)
cap.set(3, 200)
cap.set(4, 150)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8000))
s.listen(3)
clt, adr = s.accept()

time.sleep(5)
while (True):
    ret, frame = cap.read()
    clt.send(pickle.dumps("b1"))
    frame = cv2.imencode('.jpg', frame)
    frame = pickle.dumps(frame)
    clt.sendall(frame)

clt.close()
cap.release()
