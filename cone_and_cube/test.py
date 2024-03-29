import numpy
import cv2

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

widthMid = int(width/2)
heightMid = int(height/2)
midwidth = (widthMid, 0)
botwidth = (widthMid, height)
leftheight = (heightMid, 0)
rightheight = (heightMid, width)
    
color_hsv = {
    # We put HSV format of color here. 
    "cone": {'lower': numpy.array([11, 115, 70]), 'upper': numpy.array([34, 255, 245])},
    "cube": {'lower': numpy.array([110, 40, 40]), 'upper': numpy.array([125, 250, 250])},
}

while True:
    k = cv2.waitKey(1)
    if k==27:
        break
    res, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    median = cv2.medianBlur(hsv, 33)
    gauss = cv2.GaussianBlur(median, (33, 33), 1)
    erode = cv2.erode(gauss, None, iterations=1)
    cone_hsv = cv2.inRange(erode, color_hsv['cone']['lower'], color_hsv['cone']['upper'])
    cube_hsv = cv2.inRange(erode, color_hsv['cube']['lower'], color_hsv['cube']['upper'])
    cone_thresh, cone_binary = cv2.threshold(cone_hsv, 50, 255, cv2.THRESH_BINARY)
    cone_contours, cone_hierarchy = cv2.findContours(cone_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cube_thresh, cube_binary = cv2.threshold(cube_hsv, 50, 255, cv2.THRESH_BINARY)
    cube_contours, cube_hierarchy = cv2.findContours(cube_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, cone_contours, -1, (0, 255, 0), 5)
    cv2.drawContours(frame, cube_contours, -1, (0, 255, 0), 5)
    cv2.line(frame, (widthMid, 0), (widthMid, height), (58, 30, 196), 2)
    cv2.line(frame, (0, heightMid), (width, heightMid), (58, 30, 196), 2)
    #cv2.imshow("image", numpy.hstack((cone_canny, cube_hsv)))
    cv2.imshow("come", frame)
    cv2.waitKey(1)
    
cap.release()
cv2.destroyAllWindows()