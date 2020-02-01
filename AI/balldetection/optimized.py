import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):

    _, frame = cap.read()
    frame=cv2.GaussianBlur(frame, (5,5), 0)
    hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HLS_FULL)

    greenlower = np.array([42, 80, 61])
    greenupper = np.array([67, 226, 255])
    # greenlower = np.array([29, 37, 63])
    # greenupper = np.array([145, 255, 255])
    mask = cv2.inRange(hsv, greenlower, greenupper)

    kernel = np.ones((5,5), np.uint8)
    mask=cv2.erode(mask,kernel,iterations = 1)
    mask=cv2.dilate(mask, kernel, iterations=5)
    mask = cv2.erode(mask, kernel, iterations=3)

    ret, thresh = cv2.threshold(mask, 200, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = float(w) / h
        (x,y),radius =cv2.minEnclosingCircle(c)
        x= np.int(x)
        y= np.int(y)
        radius=np.int(radius)
        areac=M["m00"]
        aream=np.pi*radius**2
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
        solidity = 0
        if hull_area!=0:
            solidity = float(areac) / hull_area
        print((x,y), '\t', (cX,cY), '\t', areac, '\t', aream, '\t', aspect_ratio, '\t', solidity)
        if(aream>1000):
            if((cX<x+2) and (cX>x-2) and (cY>y-2) and (cY<y+2) and (aream)<=(areac+1500) and aspect_ratio>1 and areac>1000):
                cv2.circle(frame, (cX, cY), radius, (255, 0, 0), thickness=4)
                cv2.putText(frame,"BALL",(int(x-radius),int(y-radius)),cv2.FONT_HERSHEY_COMPLEX,0.75,(0,255,0))
                cv2.circle(frame, (cX, cY), 3, (0, 255, 0), thickness=-1)
                cv2.circle(frame, (x, y), 3, (0, 0, 255), thickness=-1)
                cv2.putText(frame, "BALL DETECTED", (500, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5,(0, 0, 255), thickness=2)


    cv2.drawContours(res, contours, -1, (0, 0, 255), 1)

    cv2.imshow('mask', res)
    cv2.imshow('hsv', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
