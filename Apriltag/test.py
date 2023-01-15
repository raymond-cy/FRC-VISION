import pupil_apriltags as apriltag
import cv2

img = cv2.imread("test.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

detector = apriltag.Detector(families='tag36h11')

tags = detector.detect(gray)

for tag in tags:
    cv2.circle(img, tuple(tag.corners[0].astype(int)), 4, (255, 0, 255), 2)  # left-top
    cv2.circle(img, tuple(tag.corners[1].astype(int)), 4, (255, 0, 255), 2)  # right-top
    cv2.circle(img, tuple(tag.corners[2].astype(int)), 4, (255, 0, 255), 2)  # right-bottom
    cv2.circle(img, tuple(tag.corners[3].astype(int)), 4, (255, 0, 255), 2)  # left-bottom

cv2.imshow("out_image", img)
cv2.imwrite("test_new.png", img)
cv2.waitKey()