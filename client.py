import socket
import pickle
import cv2
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 8000))

data = []
while True:
    packet = s.recv(4096)
    if not packet: break
    data.append(packet)
data_arr = pickle.loads(b"".join(data))
cv2.imshow('frame', data_arr)
cv2.waitKey()
cv2.destroyAllWindows()
s.close()