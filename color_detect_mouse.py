import cv2
import numpy as np
data = []
evt = -1
coord = []
img = np.zeros((250, 250, 3), np.uint8)
def click(event, x, y, flags, params):
    global pnt
    global evt
    if event==cv2.EVENT_LBUTTONDOWN:
        print("Mouse Event Was: ", event)
        print(x, ',', y)
        pnt = (x,y)
        coord.append(pnt)
        print(coord)
        evt = event
    if event==cv2.EVENT_RBUTTONDOWN:
        print("Mouse Event Was: ", event)
        print(x,y)
        blue = frame[y,x, 0]
        green = frame[y,x,1]
        red = frame[y,x,2]
        print(blue, green, red)
        colorString = str(blue)+', '+str(green)+', '+str(red)
        img[:] = [blue, green, red]
        fnt = cv2.FONT_HERSHEY_PLAIN
        r = 255-int(red)
        g = 255-int(green)
        b = 255-int(blue)
        tp = (b,g,r)
        cv2.putText(img, colorString, (10, 25), fnt, 1, tp, 1)

width = 320
height = 240

cv2.namedWindow("Cam")
cv2.setMouseCallback("Cam", click)

#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=59/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(3)
while True:
    ret, frame = cam.read()
    for pnts in coord:
        cv2.circle(frame, pnts, 3, (58, 30, 196), -1)
        font = cv2.FONT_HERSHEY_PLAIN
        myStr = str(pnts)
        cv2.putText(frame, myStr, pnts, font, 1.5, (187, 197, 57), 2)
    '''if evt==1:
        cv2.circle(frame, pnt, 3, (58, 30, 196), -1)
        font = cv2.FONT_HERSHEY_PLAIN
        myString = str(pnt)
        cv2.putText(frame, myString, pnt, font, 1, (187, 197, 177), 2)'''
    cv2.imshow("Cam", frame)
    cv2.imshow("Color", img)
    cv2.moveWindow("Cam", 0,0)
    keyEvent = cv2.waitKey(1)
    if keyEvent==ord('q'):
        break
    if keyEvent==ord('c'):
        coord = []
    if keyEvent==ord('s'):
        data.append(coord)
        print(data)
        coord = []

cam.release()
cv2.destroyAllWindows()