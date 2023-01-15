import cv2
import pupil_apriltags as apriltag

image = cv2.imread('test.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 创建一个apriltag检测器，然后检测AprilTags
options = apriltag.Detector(families='tag36h11')  # windows
results = options.detect(gray)
print(results)

for r in results:
    # 获取4个角点的坐标
    b = (tuple(r.corners[0].astype(int))[0], tuple(r.corners[0].astype(int))[1])
    c = (tuple(r.corners[1].astype(int))[0], tuple(r.corners[1].astype(int))[1])
    d = (tuple(r.corners[2].astype(int))[0], tuple(r.corners[2].astype(int))[1])
    a = (tuple(r.corners[3].astype(int))[0], tuple(r.corners[3].astype(int))[1])

    # 绘制检测到的AprilTag的框
    cv2.line(image, a, b, (255, 0, 255), 2, lineType=cv2.LINE_AA)
    cv2.line(image, b, c, (255, 0, 255), 2, lineType=cv2.LINE_AA)
    cv2.line(image, c, d, (255, 0, 255), 2, lineType=cv2.LINE_AA)
    cv2.line(image, d, a, (255, 0, 255), 2, lineType=cv2.LINE_AA)

    # 绘制 AprilTag 的中心坐标
    (cX, cY) = (int(r.center[0]), int(r.center[1]))
    cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

    # 在图像上绘制标文本
    tagFamily = r.tag_family.decode("utf-8")
    cv2.putText(image, tagFamily, (a[0], a[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imwrite('test_line.png', image)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()