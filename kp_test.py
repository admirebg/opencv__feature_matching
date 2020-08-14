import numpy as np
import cv2 as cv
import sys
from bag_object import *

focus_option = sys.argv[1]

img1_path = '/Users/kim-yeseul/Documents/user_lv/metis_monogram.jpeg'
img2_path = '/Users/kim-yeseul/Documents/metis_crop/metis_monogram/모노그램 메티스 포쉐트14.jpeg'

img1 = cv.imread(img1_path,0)     # queryImage
img2 = cv.imread(img2_path,0)     # trainImage
# img1 = cv.resize(img1, (550, 550))

height1, width1 = img1.shape
height2, width2 = img2.shape

if focus_option == "-g":
    # input image crop
    boundary_list = localize_objects(img1_path)
    l_x = round(boundary_list[0].x * width1)
    l_y = round(boundary_list[0].y * height1)
    r_x = round(boundary_list[2].x * width1)
    r_y = round(boundary_list[2].y * height1)
    img1 = img1[l_y:r_y, l_x:r_x]
    """
    boundary_list = localize_objects(img2_path)
    l_x = round(boundary_list[0].x * width2)
    l_y = round(boundary_list[0].y * height2)
    r_x = round(boundary_list[2].x * width2)
    r_y = round(boundary_list[2].y * height2)
    img2 = img2[l_y:r_y, l_x:r_x]
    """

height1, width1 = img1.shape
h_half1 = round(height1/2)
w_half1 = round(width1/2)
height2, width2 = img2.shape
h_half2 = round(height2/2)
w_half2 = round(width2/2)

print(height1, width1)
print(height2, width2)
"""
sub_img1 = img1[0:h_half, 0:w_half]
sub_img2 = img1[0:h_half, w_half:width]
sub_img3 = img1[h_half:height, 0:w_half]
sub_img4 = img1[h_half:height, w_half:width]
"""
img1_up = img1[0:h_half1, 0:width1]
img1_down = img1[h_half1:height1, 0:width1]
img2_up = img2[0:h_half2, 0:width2]
img2_down = img2[h_half2:height2, 0:width2]

height1, width1 = img1_up.shape
print(height1, width1)
height2, width2 = img2_up.shape
print(height2, width2)

cv.imshow('sub_img', img1_up)
cv.waitKey(0)
cv.imshow('sub_img', img1_down)
cv.waitKey(0)
cv.imshow('sub_img', img2_up)
cv.waitKey(0)
cv.imshow('sub_img', img2_down)
cv.waitKey(0)

img1_up = cv.resize(img1_up, (width1*2, height1*2))
img2_up = cv.resize(img2_up, (width2*2, height2*2))


height1, width1 = img1_down.shape
print(height1, width1)
height2, width2 = img2_down.shape
print(height2, width2)

img1_down = cv.resize(img1_down, (width1*2, height1*2))
img2_down = cv.resize(img2_down, (width2*2, height2*2))


# Initiate ORB detector
orb = cv.ORB_create()
# find the keypoints and descriptors with ORB
kp1_up, des1_up = orb.detectAndCompute(img1_up,None)
kp2_up, des2_up = orb.detectAndCompute(img2_up,None)

kp1_down, des1_down = orb.detectAndCompute(img1_down,None)
kp2_down, des2_down = orb.detectAndCompute(img2_down,None)

# create BFMatcher object
# crossCheck는 결과를 상위 여러개
# bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
bf = cv.BFMatcher(cv.NORM_HAMMING)

# Match descriptors
matches_up = bf.match(des1_up, des2_up)
matches_down = bf.match(des1_down, des2_down)
# print(len(matches))

# Sort them in the order of their distance.
matches_up = sorted(matches_up, key=lambda x: x.distance)
matches_down = sorted(matches_down, key=lambda x: x.distance)

v_sum_up = 0
v_sum_down = 0

for i in range(0, 30):
    print('[',i,']', matches_up[i].distance)
    v_sum_up = v_sum_up + matches_up[i].distance

for i in range(0, 30):
    print('[',i,']', matches_down[i].distance)
    v_sum_down = v_sum_down + matches_down[i].distance

up_avg = round(v_sum_up/30, 2)
down_avg = round(v_sum_down/30, 2)
total_avg = round((up_avg + down_avg)/2, 2)

print('up avg', up_avg)
print('down avg', down_avg)
print('total avg', total_avg)
# tup.append((item, v_sum / 30))
# Draw first 10 matches.
img3 = cv.drawMatches(img1_up,kp1_up,img2_up,kp2_up,matches_up[:30],None,flags=2)
img4 = cv.drawMatches(img1_down,kp1_down,img2_down,kp2_down,matches_down[:30],None,flags=2)
# plt.imshow(img3), plt.show()

cv.imshow('img_up', img3)
cv.waitKey(0)

cv.imshow('img_down', img4)
cv.waitKey(0)
