import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageQt

def seg_kmeans_color(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # 变换图像通道bgr->rgb
    b, g, r = cv2.split(img)
    img = cv2.merge([r, g, b])

    # 3个通道展平
    img_flat = img.reshape((img.shape[0] * img.shape[1], 3))
    img_flat = np.float32(img_flat)

    # 迭代参数
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 20, 0.5)
    flags = cv2.KMEANS_RANDOM_CENTERS

    # 聚类,这里k=2
    compactness, labels, centers = cv2.kmeans(img_flat, 2, None, criteria, 10, flags)

    # 显示结果
    img_output = labels.reshape((img.shape[0], img.shape[1]))
    # print(img_output)
    b = img[:, :, 0]  # 蓝通道
    g = img[:, :, 1]  # 绿通道
    r = img[:, :, 2]  # 红通道
    channels=cv2.split(img)
    b1=b*img_output
    g1=g*img_output
    r1=r*img_output

    # print(b1,g1,r1)
    img_output = cv2.merge([b1, g1, r1])
    img_output = Image.fromarray(np.uint8(img_output))
    img_pix = ImageQt.toqpixmap(img_output)
    return img_pix
    # plt.subplot(121), plt.imshow(img), plt.title('input')
    # plt.subplot(122), plt.imshow(img_output), plt.title('kmeans')
    #
    # plt.show()
if __name__ == '__main__':
    img = seg_kmeans_color(r'E:\intership_summer\BSDS300\images\train\2092.jpg')


