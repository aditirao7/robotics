import socket
import pickle
import cv2
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 8000))

while 1:
    data = []
    while True:
        packet = s.recv(65535)
        try:
            if(pickle.loads(packet) == "b1"): break
        except:
            pass
        if not packet: break
        data.append(packet)
    try:
        data_arr = pickle.loads(b"".join(data))
        data_arr = cv2.imdecode(data_arr[1],cv2.IMREAD_ANYCOLOR)
        data_arr = cv2.resize(data_arr,(640,480))
        cv2.imshow('frame',data_arr)
    except:
        pass
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cv2.destroyAllWindows()
s.close()
