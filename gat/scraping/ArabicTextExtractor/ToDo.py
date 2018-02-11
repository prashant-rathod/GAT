#TODO: Use this to figure out opencv contour labeling for individual characters
#TODO: http://blog.ayoungprogrammer.com/2013/01/equation-ocr-part-1-using-contours-to.html/
#TODO: http://www.danvk.org/2015/01/07/finding-blocks-of-text-in-an-image-using-python-opencv-and-numpy.html

import cv2
import numpy as np
from matplotlib import pyplot as plt
import scipy.ndimage
import os
from PIL import Image
import itertools

class Rectangle:
    def __hash__(self):
        return hash((self.x1,self.x2,self.y1,self.y2))
    def intersection(self, other):
        a, b = self, other
        x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
        y1 = max(min(a.y1, a.y2), min(b.y1, b.y2))
        x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
        y2 = min(max(a.y1, a.y2), max(b.y1, b.y2))
        if x1<x2 and y1<y2:
            return type(self)(x1, y1, x2, y2)
    __and__ = intersection

    def union(self, other):
        if self.intersection(other) is not None:
            return Rectangle(min(self.x1,other.x1),min(self.y1,other.y1), max(self.x2,other.x2), max(self.y2,other.y2))
        else:
            return self


    def difference(self, other):
        inter = self&other
        if not inter:
            yield self
            return
        xs = {self.x1, self.x2}
        ys = {self.y1, self.y2}
        if self.x1<other.x1<self.x2: xs.add(other.x1)
        if self.x1<other.x2<self.x2: xs.add(other.x2)
        if self.y1<other.y1<self.y2: ys.add(other.y1)
        if self.y1<other.y2<self.y2: ys.add(other.y2)
        for (x1, x2), (y1, y2) in itertools.product(
            pairwise(sorted(xs)), pairwise(sorted(ys))
        ):
            rect = type(self)(x1, y1, x2, y2)
            if rect!=inter:
                yield rect
    __sub__ = difference

    def __init__(self, x1, y1, x2, y2):
        if x1>x2 or y1>y2:
            raise ValueError("Coordinates are invalid")
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __iter__(self):
        yield self.x1
        yield self.y1
        yield self.x2
        yield self.y2

    def __eq__(self, other):
        return isinstance(other, Rectangle) and tuple(self)==tuple(other)
    def __ne__(self, other):
        return not (self==other)

    def __repr__(self):
        return type(self).__name__+repr(tuple(self))

def pairwise(iterable):
    # https://docs.python.org/dev/library/itertools.html#recipes
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

filepath = '/home/cheesecake/Downloads/AHTD3A0323_Para4.jpg'

os.system("python CroptoTextBlock.py /home/cheesecake/Downloads/AHTD3A0323_Para4.jpg")

filepath = filepath.replace('.jpg', '.crop.png')


image = cv2.imread(filepath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
edges = cv2.Canny(thresh, 100, 255)
_, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

img1 = image.copy()

cv2.drawContours(img1, contours, -1, (0,255,0), 3)
rectList = list()
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)

    rectList.append(Rectangle(x,y,x+w,y+h))
    #cv2.rectangle(img1, (x, y), (x + w, y + h), 155, 2)

def unionize(rectList):
    unionRects = list()
    for i in range(len(rectList)):
        biggestRect = rectList[i]
        for j in range(len(rectList)):
            biggestRect = biggestRect.union(rectList[j])
        unionRects.append(biggestRect)
    unionRects = set(unionRects)
    unionRects = list(unionRects)
    return unionRects

for i in range(3):
    rectList = unionize(rectList)

for rect in rectList:
    cv2.rectangle(img1, (rect.x1, rect.y1), (rect.x2,rect.y2),155, 2)


#TODO: Figure out how to include the dots (maybe if something is smaller than a certain size
#Todo: it gets added to the closest contour that can be found)

cv2.imshow("Bois", img1)
cv2.waitKey(0)