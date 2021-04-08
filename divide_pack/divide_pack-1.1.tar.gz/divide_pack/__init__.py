# !/usr/bin/python
# _*_coding:utf-8 _*_
import os
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import random


def car_hood(w, h, a, b, GrayImage):
    h_data = [0 for z in range(0, w)]
    for i in range(a, b):
        for y in range(h):
            h_data[i] += GrayImage[i, y]
    return h_data.index(max(h_data))


def point(a, b, y1, y2):
    prev_dif, new_dif = None, None
    intersections = []
    for i in range(a, b):
        prev_dif = y1[i] - y2[i]
        new_dif = y1[i + 1] - y2[i + 1]
        if abs(new_dif) < 1e-12:
            intersections.append(i)
        elif (prev_dif > 0 and new_dif < 0) or (prev_dif < 0 and new_dif > 0):
            intersections.append(i + 1)
    return intersections


def divide_gtd(y_data, n, guantongdao1):
    left = []
    right = []
    diff = []
    for i in range(len(n)):
        left.append(sum(y_data[n[i]:n[i] + guantongdao1 // 2]))
        right.append(sum(y_data[n[i] + guantongdao1 // 2:n[i] + guantongdao1]))
        diff.append(abs(left[i] - right[i]))
    return n[diff.index(min(diff))]


def list_index_2(a):
    end = None
    if len(a) == 2:
        pass
    elif len(a) > 2:
        for i in range(len(a) - 1):
            diff1 = a[i + 1] - a[i]
            if diff1 > 500:
                end = a[i + 1]
        a = [a[0], end]
    else:
        print("数据格式有误")
    return a


def zxj_divide(dir, img):
    GrayImage_zxj = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将img图像转换为灰度图，输出为GrayImage
    name = random.randint(0, 20)
    w, h = GrayImage_zxj.shape
    print(w, h)
    x_data = []
    point = [0]
    y_data = [0 for z in range(0, w)]
    for i in range(w):
        x_data.append(i)
        y_data[i] = GrayImage_zxj[i, 680]
    y_data = np.array(y_data).astype(np.int)
    # 区域一point
    for i in range(w - 1):
        if y_data[i] - y_data[i + 1] > 15:
            point.append(i)
            break
        else:
            continue
    # 区域二point
    for i in range(w - 1, -1, -1):
        if y_data[i] - y_data[i - 1] > 15:
            point.append(i)
            break
        else:
            continue
    point.append(w)
    print(point)
    for i in range(len(point) - 1):
        # plt.imshow(img[point[i]:point[i + 1]])
        # plt.show()
        cv2.imwrite(os.path.join(dir, 'part/', '{}{}.png'.format(name, i)), img[point[i]:point[i + 1]])


def main():
    group_n = 3
    chetou = 3000
    chewei = 3800
    dianchibao = 5000
    guantongdao1 = 2400
    guantongdao2 = 2700
    dir = 'D:/Image/C206/C206140800/Panoramagram/'
    path = dir + os.path.join("Panoramagram.png")
    print(path)
    img = cv2.imread(path)
    cropped = img[:, 500:3596]
    GrayImage = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)  # 将img图像转换为灰度图，输出为GrayImage
    w, h = GrayImage.shape
    print(h, w)
    # plt.imshow(cropped)
    # plt.show()
    x_data = []
    y_data = [0 for z in range(0, w)]
    c_data = [410000 for z in range(0, w)]
    g_data = [300000 for z in range(0, w)]
    for x in range(w):
        x_data.append(x)
        for y in range(h):
            y_data[x] += GrayImage[x, y]
    print("像素点计算完成")
    divide_point = []
    a = [0, w]
    divide_point.extend(a)
    car_index1 = car_hood(w, h, 0, chetou, GrayImage) + 700
    divide_point.append(car_index1)
    # x_data = np.array(x_data)
    y_data = np.array(y_data)
    c_data = np.array(c_data)
    point_d1 = list_index_2(point(6000, 14000, c_data, y_data))
    print(point_d1)
    divide_point.extend(point_d1)
    point_g1 = divide_gtd(y_data, point(17000, 20000, y_data, g_data), guantongdao1)
    divide_point.append(point_g1)
    divide_point.append(point_g1 + guantongdao1)
    point_d2 = list_index_2(point(25000, 33000, c_data, y_data))
    print(point_d2)
    divide_point.extend(point_d2)
    car_index2 = car_hood(w, h, w - chewei, w, GrayImage) - 700
    divide_point.append(car_index2)
    divide_point.sort()
    print(divide_point)
    for i in range(len(divide_point) - 1):
        cv2.imwrite(os.path.join(dir, 'result{}.png'.format(i)), cropped[divide_point[i]:divide_point[i + 1]])
    for i in range(1, len(divide_point) - 1, 2):
        zxj_divide(dir, cropped[divide_point[i]:divide_point[i + 1], :])


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end-start)
    print("执行完毕")

