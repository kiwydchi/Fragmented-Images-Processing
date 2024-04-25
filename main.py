import cv2
import glob
import numpy as np


image_paths = glob.glob('unstitchedImages/*.png')
images = []

for image in image_paths:
    img = cv2.imread(image)
    images.append(img)
    cv2.imshow("Image", img)
    cv2.waitKey()

imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

if not error:

    #cv2.imwrite("stitchedOutput.png", stitched_img)
    cv2.imshow("Stitched Image", stitched_img)
    cv2.waitKey(0)
'''

img1 = cv2.imread("GrayBot.png")
img2 = cv2.imread("GrayTop.png")
#first = cv2.imread("stitchedOutput.png")
#second = cv2.imread("board1top.png")

alpha = 1.5 # Contrast control (1.0-3.0)
beta = 0 # Brightness control (0-100)

#contrast1 = cv2.convertScaleAbs(img1, alpha=alpha, beta=beta)
#contrast2 = cv2.convertScaleAbs(img2, alpha=alpha, beta=beta)

thresh1 = cv2.threshold(img1, 120, 255, cv2.THRESH_BINARY)[1]
thresh1 = cv2.erode(thresh1, None, iterations=1)
thresh1 = cv2.dilate(thresh1, None, iterations=2)
cv2.imshow("thresh", thresh1)
cv2.waitKey(0)
thresh2 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY)[1]
#thresh2 = cv2.erode(thresh2, None, iterations=1)
thresh2 = cv2.dilate(thresh2, None, iterations=1)
cv2.imshow("thresh", thresh2)
cv2.waitKey(0)
#cv2.imwrite("contrast1.png", contrast1)
#cv2.imwrite("contrast2.png", contrast2)

sift = cv2.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(img1, mask = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY))
kp_2, desc_2 = sift.detectAndCompute(img2, mask = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY))

print("Кол-во ключевых точек на 1-м изображении:" + str(len(kp_1)))
print("Кол-во ключевых точек на 2-м изображении:" + str(len(kp_2)))

index_params = dict(algorithm=0, trees=5)
search_params = dict()

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc_1, desc_2, k=2)

good_points = []
for m, n in matches:
    if m.distance < 0.5*n.distance:
        good_points.append(m)

number_keypoints = 0
if len(kp_1) <= len(kp_2):
    number_keypoints = len(kp_1)
else:
    number_keypoints = len(kp_2)

print("Совпадающих точек:", len(good_points))
print("точки:", number_keypoints)

print("Точность совпадения:", len(good_points) / number_keypoints * 100)

result = cv2.drawMatches(img1, kp_1, img2, kp_2, good_points, None)

cv2.imshow("Result", result)
cv2.waitKey(0)

img_rgb = cv2.imread('board1top.png')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('template2.png', cv2.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]
 
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
 cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
 
cv2.imwrite('res1-1.png',img_rgb)
'''

#img1 = cv2.imread("stitchedOutput.png")
#img2 = cv2.imread("board1top.png")

#cv2.imwrite("GrayBot.png", cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
#cv2.imwrite("GrayTop.png", cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY))