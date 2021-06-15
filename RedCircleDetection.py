import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def empty(a):
    pass

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        par = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03*par, True)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 1000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 7)
            print(len(approx))
        if  6 < len(approx) < 16:
            cv2.putText(imgContour, "Circle", (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.putText(imgContour, ".", (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 8)

            
cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",900,316)
cv2.createTrackbar("threshold1", "Trackbar", 150, 255, empty)
cv2.createTrackbar("threshold2", "Trackbar", 255, 255, empty)

while True:
    _, frame = cap.read()
    imgContour = frame.copy()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv_frame = cv2.GaussianBlur(hsv_frame, (7,7), 1)
    
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    low_red1 = np.array([0, 146, 191])
    high_red2 = np.array([179, 207, 255])
    red_mask1 = cv2.inRange(hsv_frame, low_red, high_red)
    red_mask2 = cv2.inRange(hsv_frame, low_red1, high_red2)
    red_mask = red_mask1 | red_mask2
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    
    imgBlur = cv2.GaussianBlur(red, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("threshold1", "Trackbar")
    threshold2 = cv2.getTrackbarPos("threshold2", "Trackbar")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)

    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil,imgContour)

    img_height, img_width, _=hsv_frame.shape
    parametre = (img_height * img_width) * 0.03
    
    countRed = cv2.countNonZero(red_mask)
    if countRed > parametre:
        print("Red found")

    #cv2.imshow("Red", red)
    cv2.imshow("imgCanny", imgCanny)
    cv2.imshow("imgContour", imgContour)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()