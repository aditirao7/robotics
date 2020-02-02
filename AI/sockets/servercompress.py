import socket
import cv2
import numpy as np
import pickle
import time

s = socket.socket()
s.bind(('', 7000))
s.listen(3)
clt, adr= s.accept()

cap = cv2.VideoCapture(0)

cap.set(3,200)
cap.set(4,150)
time.sleep(5)

while 1:
    _, frame = cap.read()
    frame = cv2.imencode('.jpg', frame)
    frame_size = pickle.dumps(np.size(frame[1]))
    print(np.size(frame[1]))
    frame = pickle.dumps(frame)
    clt.sendall(frame_size)
    time.sleep(0.01)
    answer = clt.recv(8)
    clt.sendall(frame)

clt.close()
s.close()
cap.release()
