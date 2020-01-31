import cv2
import numpy as np

m =0
aspect_ratio = 0
def nothing(x):
    pass
def save(x):
    if(x==1):
        Thresh1 = np.array([lh,ls,lv])
        Thresh2 = np.array([uh,hs,hv])
        print(Thresh1)
        print(Thresh2)
cv2.namedWindow("HSV")
cv2.createTrackbar("lh", "HSV",0, 179, nothing);
cv2.createTrackbar("ls", "HSV",0, 255, nothing);
cv2.createTrackbar("lv", "HSV",0, 255, nothing);
cv2.createTrackbar("uh", "HSV",179, 179, nothing);
cv2.createTrackbar("hs", "HSV",255, 255, nothing);
cv2.createTrackbar("hv", "HSV",255, 255, nothing);
cv2.createTrackbar("save","HSV",0,1,save);

cv2.setTrackbarPos('lh',"HSV",25)
cv2.setTrackbarPos('ls',"HSV",80)
cv2.setTrackbarPos('lv',"HSV",58)
cv2.setTrackbarPos('uh',"HSV",47)
cv2.setTrackbarPos('hs',"HSV",219)
cv2.setTrackbarPos('hv',"HSV",255)

cap = cv2.VideoCapture(0)
while(1):

    _, frame = cap.read()
    frame=cv2.GaussianBlur(frame, (5,5), 0)
    hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HLS_FULL)

    lh = cv2.getTrackbarPos('lh', "HSV")
    ls = cv2.getTrackbarPos('ls', "HSV")
    lv = cv2.getTrackbarPos('lv', "HSV")
    uh = cv2.getTrackbarPos('uh', "HSV")
    hs = cv2.getTrackbarPos('hs', "HSV")
    hv = cv2.getTrackbarPos('hv', "HSV")

    thresh1 = np.array([lh, ls, lv])
    thresh2 = np.array([uh, hs, hv])
    mask = cv2.inRange(hsv, thresh1, thresh2)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=5)
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
        (x, y), radius = cv2.minEnclosingCircle(c)
        x = np.int(x)
        y = np.int(y)
        radius = np.int(radius)
        areac = M["m00"]
        aream = np.pi * radius ** 2
        area = cv2.contourArea(c)
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
        solidity = 0
        if hull_area != 0:
            solidity = float(area) / hull_area
        print((x, y), '\t', (cX, cY), '\t', areac, '\t', aream, '\t', solidity)
        if (aream > 1000):
            if ((cX < x + 5) and (cX > x - 5) and (cY > y - 5) and (cY < y + 5) and (aream) <= (areac + 2500) and solidity > 0.95 and areac > 3000):
                cv2.circle(res, (cX, cY), radius, (255, 0, 0), 4)
                cv2.putText(res, "BALL", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.circle(res, (cX, cY), 3, (0, 255, 0), -1)
                cv2.circle(res, (x, y), 3, (0, 0, 255), -1)

    cv2.drawContours(res, contours, -1, (0, 0, 255), 1)

    cv2.imshow('mask', mask)
    cv2.imshow('hsv', hsv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
