import socket
import cv2
import numpy as np
import pickle

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8000))
s.listen(5)
clt,adr = s.accept()
cap = cv2.VideoCapture(0)
while (1):
    ret, frame = cap.read()
    frame=pickle.dumps(frame)
    answer=clt.recv(8)
    clt.sendall(frame)

cap.release()
clt.close()
s.close()
