import cv2
import glob
import numpy as np


image_paths = glob.glob('img1/*.png')
images = []
for image in image_paths:
    img = cv2.imread(image)
    images.append(img)
    cv2.imshow("Image", img)
    cv2.waitKey()

imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

if not error:

    cv2.imwrite("img1Output.png", stitched_img)
    cv2.imshow("Stitched Image", stitched_img)
    cv2.waitKey(0)

img1 = cv2.imread("img1Output.png")
img2 = cv2.imread("bridge1.jpg")

sift = cv2.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(img1, None)
kp_2, desc_2 = sift.detectAndCompute(img2, None)

print("Кол-во ключевых точек на 1-м изображении:" + str(len(kp_1)))
print("Кол-во ключевых точек на 2-м изображении:" + str(len(kp_2)))

index_params = dict(algorithm=0, trees=5)
search_params = dict()

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc_1, desc_2, k=2)

good_points = []
for m, n in matches:
    if m.distance < 0.6*n.distance:
        good_points.append(m)

number_keypoints = 0
if len(kp_1) <= len(kp_2):
    number_keypoints = len(kp_1)
else:
    number_keypoints = len(kp_2)

print("Совпадающих точек:", len(good_points))
#print("точки:", number_keypoints)

print("Точность совпадения:", len(good_points) / number_keypoints)

result = cv2.drawMatches(img1, kp_1, img2, kp_2, good_points, matches[0:100])

cv2.imwrite("comare1.png", result)
#cv2.imshow("Result", cv2.resize(image, (1000, 1000), interpolation= cv2.INTER_LINEAR))
cv2.waitKey(0)
'''
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