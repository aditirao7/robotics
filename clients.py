import socket
import pickle
import cv2
import numpy as np


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 8000))
while (1):
    data = []
    size=0
    packet= s.recv(4096)
    frame_size=pickle.loads(packet)
    s.send(b'1')
    while size<=frame_size:
        packet = s.recv(4096)
        if not packet: break
        data.append(packet)
        size+=len(packet)
    data_arr = pickle.loads(b"".join(data))
    print(data_arr)
    cv2.imshow('frame', data_arr)
    cv2.waitKey(1)
