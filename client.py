import socket
import pickle
import cv2
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 6000))
while (1):
    data = []
    size=0
    #sizepacket= s.recv(8)
    #frame_size=pickle.loads(sizepacket)
    frame_size=640*480*3
    s.send(b'1')
    while size<=frame_size:
        packet = s.recv(65535)
        if not packet: break
        data.append(packet)
        size+=len(packet)
    data_arr = pickle.loads(b"".join(data))
    cv2.imshow('frame', data_arr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
s.close()