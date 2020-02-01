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
    #frame = cv2.resize(frame, (int(frame.shape[0] / 2), int(frame.shape[1]/ 2)))
    frame=pickle.dumps(frame)
    #size = pickle.dumps(np.size(frame))
    #_, frame= cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 30])
    #print(np.size(frame))
    #clt.sendall(size)
    answer=clt.recv(8)
    clt.sendall(frame)

cap.release()
clt.close()
s.close()