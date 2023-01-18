import numpy as np
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

class ColorMeter(object):
    color_hsv = {
        # We put HSV format of color here. 
        "cone": [np.array([11, 115, 70]), np.array([34, 255, 245])],
        "cube": [np.array([100, 43, 46]), np.array([155, 255, 255])],
    }
    def __init__(self, is_show=False):
        self.is_show = is_show
        self.img_shape = None

    def detect_color(self, frame):
        self.img_shape = frame.shape
        res = {}
        # convert image into HSV format
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for text, range_ in self.color_hsv.items():
            # remove the color which is out of the color which we want to detect
            mask = cv2.inRange(hsv, range_[0], range_[1])
            erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)
            dilation = cv2.dilate(erosion, np.ones((1, 1), np.uint8), iterations=2)
            target = cv2.bitwise_and(frame, frame, mask=dilation)
            # put picture which we have dealed in the binary
            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
            # find out contours in binary
            contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                # return point of image
                boxes = [
                    box
                    for box in [cv2.boundingRect(c) for c in contours]
                    if min(frame.shape[0], frame.shape[1]) / 10
                    < min(box[2], box[3])
                    < min(frame.shape[0], frame.shape[1]) / 1
                ]
                if boxes:
                    res[text] = boxes
                    if self.is_show:
                        for box in boxes:
                            x, y, w, h = box
                            # draw contour
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            # show image
                            cv2.putText(
                                frame,  # imag
                                text,  # text
                                (x, y),  # literal direction
                                cv2.FONT_HERSHEY_SIMPLEX,  # dot font
                                0.9,  # scale
                                (0, 255, 0),  # color
                                2,  # border
                            )
							
        if self.is_show:
            cv2.line(frame, (widthMid, 0), (widthMid, height), (58, 30, 196), 2)
            cv2.line(frame, (0, heightMid), (width, heightMid), (58, 30, 196), 2)
            cv2.imshow("image", frame)
            cv2.waitKey(1)
        # cv2.destroyAllWindows()
        return res

if __name__ == "__main__":
    m = ColorMeter(is_show=True)
    while True:
        k = cv2.waitKey(1)
        if k==27:
            break
        success, frame = cap.read()
        res = m.detect_color(frame)
        #print(res)

