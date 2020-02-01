import socket
import cv2
import numpy as np
import pickle

s = socket.socket()
s.bind(('', 8000))
s.listen(3)
clt, adr= s.accept()

cap = cv2.VideoCapture(0)
while 1:
    _, frame = cap.read()
    frame = cv2.imencode('.jpeg', frame)
    print(np.size(frame[1]))
    frame_size = pickle.dumps(np.size(frame[1]))
    frame = pickle.dumps(frame)
    clt.sendall(frame_size)
    answer = clt.recv(8)
    clt.sendall(frame)

clt.close()
s.close()
cap.release()
