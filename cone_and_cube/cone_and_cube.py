import cv2
import numpy
import pupil_apriltags as apriltag

cap = cv2.VideoCapture(0)
cv2.namedWindow("cone and cube", cv2.WINDOW_AUTOSIZE)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

widthMid = int(width/2)
heightMid = int(height/2)
midwidth = (widthMid, 0)
botwidth = (widthMid, height)
leftheight = (heightMid, 0)
rightheight = (heightMid, width)

coneColor = "yellow"
cube = "purple"

color_dist = {'yellow': {'Lower': numpy.array([0, 255, 255]), 'Upper': numpy.array([126, 255, 255])},
              'purple': {'Lower': numpy.array([129, 0, 149]), 'Upper': numpy.array([219, 50, 166])},}

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        if frame is not None:
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
            erode_hsv = cv2.erode(hsv, None, iterations=2)
            
            cone_hsv = cv2.inRange(erode_hsv, color_dist[coneColor]['Lower'], color_dist[coneColor]['Upper'])
                                                                                                                                        #cube_hsv = cv2.inRange(erode_hsv, color_dist[cube]['Lower'], color_dist[cube]['Upper'])
            
            cone_cnts = cv2.findContours(cone_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                                                                                                                                        #cube_cnts = cv2.findContours(cube_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            cone_side = max(cone_cnts, key = cv2.contourArea)
            cone_rect = cv2.minAreaRect(cone_side)
            con_box = cv2.boxPoints(cone_rect)
            cv2.drawContours(frame, [numpy.int0(con_box)], -1, (230, 38, 42), 5)
                                                                                                                                        # else:
                                                                                                                                        #     ret == 0
                                                                                                                                        #     print("ret == 0")
            cv2.line(frame, (widthMid, 0), (widthMid, height), (187, 197, 57), 5)
            cv2.line(frame, (0, heightMid), (width, heightMid), (187, 197, 57), 5)
            
            cv2.imshow("cone adn cube", frame)
            cv2.waitKey(1)
        else:
            print("nothing")
    else:
        print("No Camera")

cap.release()
cv2.destroyAllWindows()