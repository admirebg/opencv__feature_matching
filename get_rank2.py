import cv2 as cv
import os
import sys
from bag_object import *
from crop_db import *


results = []
match_up_num = []
match_down_num = []
tps = []
fps = []


def sort_tuple(tup):
    return sorted(tup, key=lambda x: x[1])


# user input value

input_path = sys.argv[1]
db_dir = sys.argv[2]
output_path = sys.argv[3]
focus_option = sys.argv[4]

input_img = cv.imread(input_path, 0)

(dirName, fileName) = os.path.split(input_path)
(input_class, fileExtension) = os.path.splitext(fileName)

height1, width1 = input_img.shape

""" 
cv.imshow('sub_img_up', input_img_up)
cv.waitKey(0)
"""
ratio = 500/height1
input_img = cv.resize(input_img, (round(width1*ratio), 500))


# Initiate ORB detector
orb = cv.ORB_create()
input_kp, input_des = orb.detectAndCompute(input_img, None)


def get_score(f_path):
    db_img = cv.imread(f_path, 0)

    height2, width2 = db_img.shape

    ratio = 500/height2
    db_img = cv.resize(db_img, (round(width2*ratio), 500))

    # find the keypoints and descriptors with ORB
    db_kp, db_des = orb.detectAndCompute(db_img, None)

    # create BFMatcher object
    # bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    bf = cv.BFMatcher(cv.NORM_HAMMING)

    sum = 0

    # Match descriptors
    matches = bf.match(input_des, db_des)
    matches = sorted(matches, key=lambda x: x.distance)   # Sort them in the order of their distance.

    for u in range(0, 30):      #top30. u: 0~29
        sum = sum + matches[u].distance

    avg = round(sum / 30, 2)

    # print(f_path, len(up_matches), len(down_matches))

    # todo. up_match_len == 0 and down_match_len == 0
    print('total_avg', avg)

    return avg


sub_dirs = os.listdir(db_dir)

input_class_num = 0
same_class = False

for item in sub_dirs:
    if item[0] == '.':
        continue
    tem_path = db_dir+'/'+item
    files = os.listdir(tem_path)
    if item == input_class:
        input_class_num = len(files)
        same_class = True
    for file in files:
        if file[0] == '.':
            if same_class is True:
                input_class_num = input_class_num - 1
            continue
        file_path = tem_path+'/'+file
        ret = get_score(file_path)
        results.append((file, round(ret, 3), item))
    if same_class is True:
        same_class = False


results = sort_tuple(results)
total_num = len(results)
tem_tp = 0

for n in range(0, 20):
    # print(results[n][2])
    if results[n][2] == input_class:
        tem_tp = tem_tp + 1
    # print(n, tem_tp, n+1-tem_tp)
    tps.append(tem_tp)
    fps.append(n+1-tem_tp)


cnt = 1

# output_path = input("output: ")
f = open(output_path, 'w')


f.write('*******************************************************************\n')
f.write('input image: %s\n' % input_path)
f.write('DB directory: %s\n' % db_dir)
f.write('output file: %s\n' % output_path)
f.write('input class: %s\n' % input_class)
f.write('the number of input class: %s\n' % input_class_num)
f.write('*******************************************************************\n\n')

for i in results:
    #print(cnt, i)
    f.write('%d. ' % cnt)
    f.write('%-60s%-30s%-30s\n' % i)
    cnt = cnt + 1


f.write('*******************************************************************\n\n')
for n in range(1, 21):
    f.write('n=%d, ' % n)
    f.write('precision: %s, ' % round(tps[n-1]/n, 4))
    f.write('recall: %s, ' % round(tps[n-1]/input_class_num, 4))
    f.write('accuracy: %s\n' % round((tps[n-1]+total_num-input_class_num-fps[n-1])/total_num, 4))





