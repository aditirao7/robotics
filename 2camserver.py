import socket
import cv2
import numpy as np
import pickle

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8000))
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 7000))
sock.listen(5)
s.listen(5)
clt1,adr1 = sock.accept()
clt,adr = s.accept()
cap = cv2.VideoCapture(4)
cap1= cv2.VideoCapture(0)
while (1):
    ret, frame = cap.read()
    ret1, frame1 = cap1.read()
    #size = pickle.dumps(np.size(frame))
    frame1 = pickle.dumps(frame1)
    frame= pickle.dumps(frame)
    #clt.sendall(size)
    answer=clt.recv(8)
    clt1.sendall(frame1)
    clt.sendall(frame)

cap.release()
cap1.release()
clt.close()
s.close()
clt1.close()
sock.close()