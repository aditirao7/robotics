import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):

    _, frame = cap.read()
    frame=cv2.GaussianBlur(frame, (5,5), 0)
    hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HLS_FULL)

    greenlower = np.array([47, 46, 63])
    greenupper = np.array([74, 255, 255])
    mask = cv2.inRange(hsv, greenlower, greenupper)

    kernel = np.ones((5, 5), np.uint8)
    mask=cv2.erode(mask,kernel,iterations = 1)
    mask=cv2.dilate(mask, kernel, iterations=3)
    mask = cv2.erode(mask, kernel, iterations=2)

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
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 3, 300, param1=250, param2=40, minRadius=0, maxRadius=0)
        if circles is None:
            continue
        circles = np.uint8(np.round(circles))
        for i in circles[0, :]:
            areah=np.pi*(i[2])**2
            areac=M["m00"]
            print(areah, '\t', areac)
            if areah<=(areac+100) and areah>=(areac-100):
                cv2.circle(res, (i[0], i[1]), i[2], (255, 0, 0), 4)
                cv2.putText(res, "BALL", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.circle(res, (cX, cY), 3, (0, 255, 0), -1)

    cv2.drawContours(res, contours, -1, (0, 0, 255), 1)

    cv2.imshow('res', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
