# -*- coding: utf-8 -*-
# By:xjs

import cv2
import numpy as np
import os
import random
import time



# while True:
def test_door(image_name):
    # image_name = random.choice(os.listdir('test'))
    # print(f"获取图像文件的名字: {image_name}")
    # cv2.imshow(image_name)
    # 初始化
    standard_image = cv2.imread('weights/opencv_door/standard.jpg')
    timelimit = 10
    ifopen = False
    frame = cv2.imread(image_name)

    # frame = cv2.imread(os.path.join('test', image_name))
    fgmask = cv2.absdiff(standard_image, frame)
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]


    if np.sum(thresh) > 0:
        height, width = thresh.shape[:2]
        upper_half = thresh[0:height//2, :]
        lower_half = thresh[height//2:, :]

        if np.sum(upper_half) > np.sum(lower_half):
            print('上面的修改：',np.sum(upper_half))
            print('下面的修改：',np.sum(lower_half))

            print("外侵入开门")
            ifopen = True
            timelimit = 10
        else:
            print("内侵入开门")
            ifopen = True
            timelimit = 10
    else:
        if timelimit > 0 and ifopen == True:
            timelimit -= 1
            print(f"关门倒计时{timelimit}")
            time.sleep(1)
        elif timelimit == 0:
            ifopen == False
            print("超时关门")
# test_pic/test_image_in.jpg
# test_pic/test_image_out.jpg

# test_door("test_pic/test_image_in.jpg")

