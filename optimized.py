import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):

    _, frame = cap.read()
    frame=cv2.GaussianBlur(frame, (5,5), 0)
    hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HLS_FULL)

    greenlower = np.array([32, 40, 100])
    greenupper = np.array([82, 255, 255])
    mask = cv2.inRange(hsv, greenlower, greenupper)

    kernel = np.ones((5, 5), np.uint8)
    mask=cv2.erode(mask,kernel,iterations = 1)
    mask=cv2.dilate(mask, kernel, iterations=5)
    mask = cv2.erode(mask, kernel, iterations=3)

    ret, thresh = cv2.threshold(mask, 200, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        (x,y),radius =cv2.minEnclosingCircle(c)
        x= np.int(x)
        y= np.int(y)
        radius=np.int(radius)
        areac=M["m00"]
        aream=np.pi*radius**2
        area = cv2.contourArea(c)
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
#        epsilon = 0.1 * cv2.arcLength(c, True)
#        c = cv2.approxPolyDP(c, epsilon, True)
        solidity=0
        if hull_area!=0:
            solidity = float(area) / hull_area
        print((x,y), '\t', (cX,cY), '\t', areac, '\t', aream, '\t', solidity)
        if(aream>1000):
            if((cX<x+5) and (cY<y+5) and (aream)<=(areac+2500) and solidity>0.95 and areac>3000):
                cv2.circle(res, (cX, cY), radius, (255, 0, 0), 4)
                cv2.putText(res, "BALL", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.circle(res, (cX, cY), 3, (0, 255, 0), -1)
                cv2.circle(res, (x, y), 3, (0, 0, 255), -1)

    cv2.drawContours(res, contours, -1, (0, 0, 255), 1)

    cv2.imshow('res', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()