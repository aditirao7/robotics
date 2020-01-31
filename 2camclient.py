import socket
import pickle
import cv2
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 8000))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('', 7000))
while (1):
    data = []
    size=0
    data1=[]
    size1=0
    #sizepacket= s.recv(8)
    #frame_size=pickle.loads(sizepacket)
    frame_size=640*480*3
    s.send(b'1')
    while size<=frame_size and size1<frame_size:
        packet = s.recv(65535)
        packet1= sock.recv(65535)
        if not packet: break
        if not packet1: break
        data.append(packet)
        size+=len(packet)
        data1.append(packet1)
        size1 += len(packet1)
    data_arr = pickle.loads(b"".join(data))
    data_arr1= pickle.loads(b"".join(data1))
    cv2.imshow('frame', data_arr)
    cv2.imshow('frame1', data_arr1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
s.close()
sock.close()