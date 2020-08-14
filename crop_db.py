import sys
import cv2 as cv
from bag_object import *

# input_path = sys.argv[1]
# output_path = sys.argv[2]


# 새로운 디렉토리 생성
def mk_dir(path):
    try:
        if not(os.path.isdir(path)):
            os.makedirs(os.path.join(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise


# input_path 디렉토리의 사진들을 crop하여 output_path 디렉토리로 생성
def make_crop_db(input_path, output_path):
    mk_dir(output_path)

    sub_dirs = os.listdir(input_path)

    for item in sub_dirs:
        if item[0] == '.':
            continue
        tem_path = input_path+'/'+item
        files = os.listdir(tem_path)
        mk_dir(output_path+'/'+item)

        for file in files:
            if file[0] == '.' or file[0] == '_':
                continue
            file_path = tem_path+'/'+file

            (filename, fileExtension) = os.path.splitext(file)

            input_img = cv.imread(file_path)
            height1, width1, channel1 = input_img.shape

            boundary_list = localize_objects(file_path, 'Bag')     # crop할 좌표값 가져옴

            if len(boundary_list) == 0:
                boundary_list = localize_objects(file_path, 'Handbag')
                if len(boundary_list) != 0:
                    l_x = round(boundary_list[0].x * width1)
                    l_y = round(boundary_list[0].y * height1)
                    r_x = round(boundary_list[2].x * width1)
                    r_y = round(boundary_list[2].y * height1)

                    input_img = input_img[l_y:r_y, l_x:r_x]

                    new_input_path = tem_path + '/' + '_' + filename + fileExtension
                    cv.imwrite(new_input_path, input_img)

                    boundary_list = localize_objects(new_input_path, 'Bag')
                    height1, width1, channel1 = input_img.shape

            if len(boundary_list) == 0:
                continue

            l_x = round(boundary_list[0].x * width1)
            l_y = round(boundary_list[0].y * height1)
            r_x = round(boundary_list[2].x * width1)
            r_y = round(boundary_list[2].y * height1)

            input_img = input_img[l_y:r_y, l_x:r_x]
            cv.imwrite(output_path+'/'+item+'/'+file, input_img)    # crop된 사진 저장







