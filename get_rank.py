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

# google api option
if focus_option == "-g":
    # input image crop
    boundary_list = localize_objects(input_path, 'Bag')

    if len(boundary_list) == 0:
        boundary_list = localize_objects(input_path, 'Handbag')
        if len(boundary_list) != 0:
            l_x = round(boundary_list[0].x * width1)
            l_y = round(boundary_list[0].y * height1)
            r_x = round(boundary_list[2].x * width1)
            r_y = round(boundary_list[2].y * height1)
            input_img = input_img[l_y:r_y, l_x:r_x]
            input_path = dirName+'/'+input_class+'_handbag'+fileExtension
            cv.imwrite(input_path, input_img)
            boundary_list = localize_objects(input_path, 'Bag')
            height1, width1 = input_img.shape

    if len(boundary_list) == 0:
        raise Exception('bag object does not exist.')

    l_x = round(boundary_list[0].x * width1)
    l_y = round(boundary_list[0].y * height1)
    r_x = round(boundary_list[2].x * width1)
    r_y = round(boundary_list[2].y * height1)
    input_img = input_img[l_y:r_y, l_x:r_x]
    # db image crop
    if not(os.path.isdir(db_dir+'_crop')):
        make_crop_db(db_dir, db_dir+'_crop')

    db_dir = db_dir+'_crop'


height1, width1 = input_img.shape
h_half1 = round(height1/2)

input_img_up = input_img[0:h_half1, 0:width1]
input_img_down = input_img[h_half1:height1, 0:width1]


cv.imshow('sub_img_down', input_img_down)
cv.waitKey(0)
""" 
cv.imshow('sub_img_up', input_img_up)
cv.waitKey(0)
"""
ratio = 500/h_half1
input_img_up = cv.resize(input_img_up, (round(width1*ratio), 500))
input_img_down = cv.resize(input_img_down, (round(width1*ratio), 500))

# Initiate ORB detector
orb = cv.ORB_create()
input_up_kp, input_up_des = orb.detectAndCompute(input_img_up, None)
input_down_kp, input_down_des = orb.detectAndCompute(input_img_down, None)

print('input:', input_path)
print('input_up_des:', len(input_up_kp), 'input_down_des:', len(input_down_kp))


def get_score(f_path):
    db_img = cv.imread(f_path, 0)

    height2, width2 = db_img.shape
    h_half2 = round(height2 / 2)

    db_img_up = db_img[0:h_half2, 0:width2]
    db_img_down = db_img[h_half2:height2, 0:width2]

    ratio = 500/h_half2
    db_img_up = cv.resize(db_img_up, (round(width2*ratio), 500))
    db_img_down = cv.resize(db_img_down, (round(width2*ratio), 500))

    # find the keypoints and descriptors with ORB
    db_up_kp, db_up_des = orb.detectAndCompute(db_img_up, None)
    db_down_kp, db_down_des = orb.detectAndCompute(db_img_down, None)

    print('fpath:', f_path)
    print('db_up_kp:', len(db_up_kp), 'db_down_kp:', len(db_down_kp))

    # create BFMatcher object
    # bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    bf = cv.BFMatcher(cv.NORM_HAMMING)

    up_match_len = 0
    down_match_len = 0
    up_sum = 0
    down_sum = 0
    up_avg = 0
    down_avg = 0

    # Match descriptors
    if len(input_up_kp) != 0 and len(db_up_kp) != 0:
        up_matches = bf.match(input_up_des, db_up_des)
        up_matches = sorted(up_matches, key=lambda x: x.distance)   # Sort them in the order of their distance.
        up_match_len = len(up_matches)

        for u in range(0, 30):      #top30. u: 0~29
            up_sum = up_sum + up_matches[u].distance
            if u == up_match_len-1:
                break

        up_avg = round(up_sum / (u+1), 2)

    if len(input_down_kp) != 0 and len(db_down_kp) != 0:
        down_matches = bf.match(input_down_des, db_down_des)
        down_matches = sorted(down_matches, key=lambda x: x.distance)
        down_match_len = len(down_matches)

        for d in range(0, 30):
            down_sum = down_sum + down_matches[d].distance
            if d == down_match_len-1:
                break

        down_avg = round(down_sum / (d+1), 2)

    # print(f_path, len(up_matches), len(down_matches))

    if up_match_len == 0 and down_match_len != 0:
        total_avg = down_avg
    elif up_match_len != 0 and down_match_len == 0:
        total_avg = up_avg
    elif up_match_len != 0 and down_match_len != 0:
        total_avg = round((up_avg + down_avg) / 2, 2)

    # todo. up_match_len == 0 and down_match_len == 0
    print('up_avg:', up_avg, 'down_avg:', down_avg, 'total_avg', total_avg)

    return total_avg


sub_dirs = os.listdir(db_dir)

input_class_num = 5
same_class = False

for item in sub_dirs:
    if item[0] == '.':
        continue
    tem_path = db_dir+'/'+item
    files = os.listdir(tem_path)
	# if item == input_class:
	# input_class_num = len(files)
	# same_class = True
    fcnt = 0
    for file in files:
        if file[0] == '.':
		#if same_class is True:
		#input_class_num = input_class_num - 1
            continue
        file_path = tem_path+'/'+file
        ret = get_score(file_path)
        results.append((file, round(ret, 3), item))
        fcnt = fcnt + 1
        if fcnt == 5:
            break
	#if same_class is True:
	#same_class = False


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





