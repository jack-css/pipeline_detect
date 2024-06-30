import cv2
import numpy as np


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
    result_image = cv2.convertScaleAbs(gray_image, alpha=255 / (high_threshold - low_threshold), beta=-low_threshold)
    result_image[result_image < 0] = 0
    result_image[result_image > 255] = 255

    return result_image


# 读取图像
image = cv2.imread('./test.png')

# 自动分段灰度变换
result_image = auto_segment_gray_transform(image, 10, 50)  # 10% - 90% 的像素范围内进行自动分段灰度变换

# 显示结果图像
cv2.imshow('Result Image', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
