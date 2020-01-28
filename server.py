import socket
import cv2
import numpy as np
import pickle

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8000))
s.listen(5)
while True:
    clt,adr = s.accept()
    frame=cv2.imread('pixar.jpeg')
    print(frame.shape)
    frame= pickle.dumps(frame)
    clt.sendall(frame)
    clt.close()