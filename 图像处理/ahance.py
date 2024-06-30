import cv2
import os
import numpy as np

def main():
    path = r"G:\p_opencv\image_Deal"
    files = os.listdir(path)
    from natsort import natsorted

    files = natsorted(os.listdir(path))
    file = path + '\\' + files[25]
    img = cv2.imread(file)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('wef1', img)
    cv2.waitKey(0)


    dark_img = img-58

    light = auto_segment_gray_transform(img, 20, 50)
    ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    cv2.imshow('dark', dark_img)
    cv2.waitKey(12)
    cv2.imshow('light', light)
    cv2.waitKey(0)

def auto_segment_gray_transform(gray_image, percentage_low, percentage_high):
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

if __name__ == "__main__":
    main()