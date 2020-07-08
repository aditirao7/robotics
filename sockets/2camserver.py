import cv2
import threading

def cam1():
    cap = cv2.VideoCapture(4)
    while 1:
        ret, frame = cap.read()
        cv2.imshow("cam1", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return 0

def cam2():
    cap1 = cv2.VideoCapture(0)
    while 1:
        ret1, frame1 = cap1.read()
        cv2.imshow("cam2", frame1)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap1.release()
    cv2.destroyAllWindows()
    return 0

while 1:
    if __name__ == "__main__":

        t1 = threading.Thread(target=cam1, name='cam1')
        t2 = threading.Thread(target=cam2, name='cam2')

        t1.start()
        t2.start()

        if t1.isAlive()==True:
            t1.kill()
        if t2.isAlive()==True:
            t2

cv2.destroyAllWindows()