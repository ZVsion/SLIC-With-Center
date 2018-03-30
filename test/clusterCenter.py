# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:17:03 2018

@author: 57675
"""
from Farsee2SLIC import slic
from skimage.segmentation import mark_boundaries
# from skimage.segmentation import slic
from skimage import img_as_ubyte
import cv2
import numpy as np
import datetime

image = cv2.imread("bag.jpg")

starttime = datetime.datetime.now()

segments, superpixel_center, edge = slic(image, n_segments=800)
# segments = slic(image, n_segments=800)
endtime = datetime.datetime.now()
print("time:" + str((endtime - starttime).seconds))

# print(edge)
n_seg = np.amax(segments) + 1
num_seg = np.zeros(n_seg)

for x in range(0, image.shape[0]):
    for y in range(0, image.shape[1]):
        num_seg[segments[x, y]] += 1
ave_LAB = np.zeros((n_seg, 3), dtype=np.float)
for x in range(0, image.shape[0]):
    for y in range(0, image.shape[1]):
        ave_LAB[segments[x, y]] += image[x, y]
for i in range(0, n_seg):
    ave_LAB[i] /= num_seg[i]
#
# count = 0
# for i in range(len(superpixel_center)):
#     v = superpixel_center[i] - ave_LAB[i]
#     for j in range(3):
#         if v[j] > 3:
#             print(str(i) + ":" + str(v))
#             count+=1
#             break
# print(count)

superpixel_image = img_as_ubyte(mark_boundaries(image, segments))

temp_img = superpixel_image.copy()
ave_cor = [[0, 0] for i in range(0, n_seg)]
for x in range(0, len(segments)):
    for y in range(0, len(segments[0])):
        ave_cor[segments[x, y]][0] += x
        ave_cor[segments[x, y]][1] += y
for i in range(0, n_seg):
    ave_cor[i] /= num_seg[i]

for i in range(0, n_seg):
    for j in edge[i]:
        if j >= n_seg:
            print(str(i) + ":" + str(j))

for i in range(0, n_seg):
    for j in edge[i]:
        if j < i:
            continue
        # print(i)
        # print(j)
        cv2.line(temp_img, (int(ave_cor[i][1]), int(ave_cor[i][0])), (int(ave_cor[j][1]), int(ave_cor[j][0])),
                 (0, 0, 255), 1)
temp_img = temp_img.astype('uint8')

cv2.imshow("superpixel", temp_img)
cv2.waitKey(0)