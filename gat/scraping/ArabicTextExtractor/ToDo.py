#TODO: Use this to figure out opencv contour labeling for individual characters
#TODO: http://blog.ayoungprogrammer.com/2013/01/equation-ocr-part-1-using-contours-to.html/
#TODO: http://www.danvk.org/2015/01/07/finding-blocks-of-text-in-an-image-using-python-opencv-and-numpy.html

import cv2
import numpy as np
from matplotlib import pyplot as plt
import scipy.ndimage

image = cv2.imread('/home/cheesecake/Downloads/skewed.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
	angle = -(90 + angle)
else:
	angle = -angle
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# draw the correction angle on the image so we can validate it
rotated = cv2.bitwise_not(rotated)
rotated = cv2.GaussianBlur(rotated,(5,5),0)
edges = cv2.Canny(rotated, 100, 255)


def dilate(ary, N, iterations):
    kernel = np.zeros((N,N), dtype=np.uint8)
    kernel[(N-1)/2,:] = 1
    dilated_image = cv2.dilate(ary / 255, kernel, iterations=iterations)

    kernel = np.zeros((N,N), dtype=np.uint8)
    kernel[:,(N-1)/2] = 1
    dilated_image = cv2.dilate(dilated_image, kernel, iterations=iterations)
    return dilated_image

dilated = dilate(edges,N=3,iterations=100)
# show the output image
print("[INFO] angle: {:.3f}".format(angle))
cv2.imshow("Best",dilated)
cv2.waitKey(0)
