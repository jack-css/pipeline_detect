import os
import base64
import cv2
import cv2.gapi
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt


def MakeNor(image):
    # img = cv2.imread('../test0.png')
    P = [[2.58100780e+03, 0, 320],
         [0, 2.58732767e+03, 240],
         [0, 0, 1]]
    K = [-1.51904924e+01, 3.45247566e+02, 3.40699221e-02, -1.07431419e-01,
         -6.08582432e+03]
    img_distort = cv2.undistort(image, np.array(P), np.array(K))
    return img_distort


# 开启摄像头

def Get_img_FromCamera():
    # 1是第一号摄像头
    WIDTH = 300
    HEIGHT = 300
    # , cv2.CAP_DSHOW
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 打开摄像头
    # 在树莓派上没有cv2.CAP_DSHOW
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)  # 关闭自动曝光
    cv2.CAP_PROP_EXPOSURE = 180
    flag = 1
    while 1:
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        # 设置摄像头设备帧率,如不指定,默认600
        # cap.set(cv2.CAP_PROP_FPS, 600)
        # 建议使用XVID编码,图像质量和文件大小比较都兼顾的方案
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # get a frame
        # for _ in range(200):
        #     cap.grab()  # 只读取，但不使用帧数据
        ret, img = cap.read()
        # cv2.waitKey(20)
        # img = cv2.flip(img, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示
        img = MakeNor(img)
        # cv2.waitKey(2)
        # cv2.imshow('wse', img)
        flag += 1
        # cv2.calcHist(img, 3)
        cv2.imshow('origin', img)
        cv2.waitKey(2)
        if flag > 50:
            return 1


def one_pic():
    path = r"G:\p_opencv\image_Deal"
    files = os.listdir(path)
    from natsort import natsorted
    files = natsorted(os.listdir(path))
    file = path + '\\' + files[70]
    # file = r"G:\p_opencv\aready\one.png"
    img = cv2.imread(file)
    cv2.imshow('wef1', img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    # cv2.imshow('grat_img', img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = auto_segment_gray_transform(img, 60, 95)
    cv2.imshow('wef', img)
    ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    cv2.imshow('grat_img', img)
    cv2.waitKey(0)


def from_path_main():
    # path = r"G:\p_opencv\deal_20241"
    path = r"G:\p_opencv\image_Deal"
    files = os.listdir(path)
    print(files)
    i = 0
    for file in files:
        if i != 70:
            i += 1
            continue
        file = path + '\\' + file
        print(file)
        img = cv2.imread(file)
        cv2.imshow('origin_img', img)
        # cv2.waitKey(0)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = auto_segment_gray_transform(img, 20, 90)
        img[0:500, 0:80] = 200

        img = cv2.equalizeHist(img)
        cv2.imshow('wef', img)
        ret, img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)

        # img = auto_segment_gray_transform(img, 10, 80)
        cv2.imshow('la', img)
        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
        # img = cv2.Canny(img, 12, 255)
        ret, img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)

        contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        blank = np.zeros(img.shape[:2], dtype='uint8')
        for contour in contours:
            p = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter < 150 or perimeter > 2000:

                continue
            else:
                print(perimeter)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            cv2.drawContours(blank, contour, -1, (255, 255, 255), 4)
        cv2.imshow('cnny', blank)
        cv2.waitKey(1200)


def main():
    # 树莓派循迹启动
    # root = tk.Tk()
    # root.withdraw()  # 隐藏主窗口
    # messagebox.Message("启动检测车已开启")
    # result = Get_img_FromCamera()
    # from_path_main()
    one_pic()
    # if result:
    #     result_depair = messagebox.askyesno("确认", "检测到管道损坏，是否需要修补？")
    #     print(result_depair)


def auto_segment_gray_transform(image, percentage_low, percentage_high):
    # 将图像转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算图像直方图
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    # 计算累积直方图
    cumulative_hist = np.cumsum(hist)

    # 计算灰度值范围
    total_pixels = gray_image.shape[0] * gray_image.shape[1]
    low_threshold = np.argmax(cumulative_hist > (total_pixels * percentage_low / 100))
    high_threshold = np.argmax(cumulative_hist > (total_pixels * percentage_high / 100))

    # 分段灰度变换
    result_image = cv2.convertScaleAbs(gray_image, alpha=35 / (high_threshold - low_threshold),
                                       beta=-low_threshold * 2 + 40)
    result_image[result_image < 0] = 0
    result_image[result_image > 255] = 255
    cv2.destroyAllWindows()
    return result_image


def get_hist(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    # 绘制直方图
    plt.plot(hist, color='black')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()


if __name__ == "__main__":
    main()
