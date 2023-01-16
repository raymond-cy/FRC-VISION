import numpy as np
import cv2


class ColorMeter(object):

    color_hsv = {
        # HSV，H表示色调（度数表示0-180），S表示饱和度（取值0-255），V表示亮度（取值0-255）
        # "orange": [np.array([11, 115, 70]), np.array([25, 255, 245])],
        "cone": [np.array([11, 115, 70]), np.array([34, 255, 245])],
        "green": [np.array([35, 115, 70]), np.array([77, 255, 245])],
        "lightblue": [np.array([78, 115, 70]), np.array([99, 255, 245])],
        "mat": [np.array([100, 115, 70]), np.array([124, 255, 245])],
        "cube": [np.array([125, 115, 70]), np.array([155, 255, 245])],
        "red": [np.array([156, 115, 70]), np.array([179, 255, 245])],
    }

    def __init__(self, is_show=False):
        self.is_show = is_show
        self.img_shape = None

    def detect_color(self, frame):
        self.img_shape = frame.shape
        res = {}
        # 将图像转化为HSV格式
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for text, range_ in self.color_hsv.items():
            # 去除颜色范围外的其余颜色
            mask = cv2.inRange(hsv, range_[0], range_[1])

            erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)
            dilation = cv2.dilate(erosion, np.ones((1, 1), np.uint8), iterations=2)
            target = cv2.bitwise_and(frame, frame, mask=dilation)

            # 将滤波后的图像变成二值图像放在binary中
            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
            # 在binary中发现轮廓，轮廓按照面积从小到大排列
            contours, hierarchy = cv2.findContours(
                binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if len(contours) > 0:
                # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和高
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
                            # 绘制矩形框对轮廓进行定位
                            cv2.rectangle(
                                frame, (x, y), (x + w, y + h), (153, 153, 0), 2
                            )
                            # 将绘制的图像保存并展示
                            # cv2.imwrite(save_image, img)
                            cv2.putText(
                                frame,  # image
                                text,  # text
                                (x, y),  # literal direction
                                cv2.FONT_HERSHEY_SIMPLEX,  # dot font
                                0.9,  # scale
                                (255, 255, 0),  # color
                                2,  # border
                            )
        if self.is_show:
            cv2.imshow("image", frame)
            cv2.waitKey(1)
        # cv2.destroyAllWindows()
        return res


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    m = ColorMeter(is_show=True)
    while True:
        k = cv2.waitKey(1)
        if k==27:
            break
        success, frame = cap.read()
        res = m.detect_color(frame)
        print(res)

