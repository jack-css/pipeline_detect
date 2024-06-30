import cv2
import numpy as np

def two():
    path = r"G:\p_opencv\aready\two.png"
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = auto_segment_gray_transform(img, 20, 65)
    ret, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
    blank = np.zeros(img.shape[:2], dtype='uint8')
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for con in contours:
        cv2.drawContours(blank, con, -1, (255, 255, 255), 4)
    cv2.putText(blank, 'bulge', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    cv2.imshow('pone', img)
    cv2.imshow('pon1e', blank)

    cv2.waitKey(0)


def main():
    path = r"G:\p_opencv\aready\one.png"
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3,3), 0)
    img = auto_segment_gray_transform(img, 60, 95)
    ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img = cv2.Canny(img, 10, 150)
    blank = np.zeros(img.shape[:2], dtype='uint8')
    print(img.shape)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for con in contours:
        cv2.drawContours(blank, con, -1, (255, 255, 255), 4)
    blank[0:80, 0:100] = 0
    blank[140:340, 0:100] = 0
    blank[0:120, 80:200] = 0
    blank[210:290, 300:350] = 0
    cv2.putText(blank, 'crack', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    cv2.imshow('pone', img)
    cv2.imshow('pon1e', blank)

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



def show_dark():
    path = r"G:\p_opencv\del414\imh15.png"
    img = cv2.imread(path)
    # img = auto_segment_gray_transform(img,30,50)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('eg1', img)
    img = cv2.GaussianBlur(img, (7, 7), 2)
    img = cv2.medianBlur(img, 3)
    img = cv2.equalizeHist(img)
    cv2.imshow('eg', img)
    cv2.waitKey(0)

import numpy as np
import matplotlib.pyplot as plt

def load_image(filename):
    # 使用Matplotlib加载图像数据
    image = plt.imread(filename)
    # 将图像数据转换为灰度图像（如果是彩色图像）
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    # 将图像数据转换为字符串
    image_data = ''.join([format(int(pixel * 255), '08b') for pixel in np.nditer(image)])
    return image_data

def lzw_compress(data):
    dictionary = {chr(i): i for i in range(256)}  # 初始化字典，每个ASCII字符对应一个编码
    result = []  # 存储压缩后的编码序列
    buffer = ''  # 缓冲区
    compression_steps = []  # 用于存储每一步的压缩结果

    for char in data:
        buffer_plus_char = buffer + char  # 缓冲区加上当前字符
        if buffer_plus_char in dictionary:  # 如果缓冲区加上当前字符在字典中存在
            buffer = buffer_plus_char  # 更新缓冲区
        else:
            result.append(dictionary[buffer])  # 将缓冲区对应的编码加入结果
            dictionary[buffer_plus_char] = len(dictionary)  # 将缓冲区加上当前字符作为新编码加入字典
            buffer = char  # 更新缓冲区为当前字符
            compression_steps.append(result)  # 记录当前压缩结果

    if buffer:
        result.append(dictionary[buffer])  # 处理剩余的字符

    return result, compression_steps

# 绘制压缩前后的数据对比图
def plot_compression_comparison(original_data, compressed_data):
    # original_data = np.array(original_data).astype(float)
    print(original_data[:100],compressed_data[:100])
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(np.array(list(original_data)).reshape(100, 100), cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    axes[1].plot(compressed_data)
    axes[1].set_title('Compressed Data')
    plt.show()

def diff_lzw():
    # Example usage
    filename = r"G:\p_opencv\chuang\1.png"
    # Load image from file
    # 示例用法
    image_data = load_image(filename)
    compressed_data, compression_steps = lzw_compress(image_data)
    plot_compression_comparison(image_data, compressed_data)
    # with open('./1.txt', 'w') as f:
    #     f.write(str(compressed_data))
    #     f.write('\n\n')
    #     f.write(str(image_data))
    # print(image_data)
    # print(compressed_data)


if __name__ == "__main__":
    diff_lzw()
    # show_dark()
    # main()
    # two()