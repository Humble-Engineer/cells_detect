import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class Statistics:

    def __init__(self, main_window):

        self.main_window = main_window

    def fast_fft(self):
        """
        使用OpenCV对给定的图像进行傅里叶变换（快速傅里叶变换），并使用matplotlib显示频谱图像。
        可选地，可以指定裁剪大小来放大显示幅度谱的中间部分。

        参数:
            image (numpy.ndarray): 输入图像，应为二维灰度图像或三维彩色图像（BGR顺序）
            crop_size (tuple, optional): 裁剪区域的大小，格式为 (height, width)，默认为 None（不裁剪）
        """
        self.main_window.camera.stop_thread() # 先关闭实时捕获功能防止图像被覆盖
        self.main_window.basic.reset_image()

        img = cv.cvtColor(self.main_window.result_img, cv.COLOR_BGR2GRAY)

        # 确保图像为浮点类型，便于进行数学运算
        image_float = img.astype(np.float32)

        crop_size = (16, 16)

        # 将图像扩展为偶数尺寸，以避免边缘效应
        height, width = image_float.shape[:2]
        pad_height = (height % 2) * (height // 2)
        pad_width = (width % 2) * (width // 2)
        padded_image = np.pad(image_float, ((0, pad_height), (0, pad_width)), mode='constant')

        # 进行离散傅里叶变换（DFT），得到复数形式的频谱
        dft_img = cv.dft(padded_image, flags=cv.DFT_COMPLEX_OUTPUT)

        # 提取实部和虚部，以便分别显示
        real_part = np.abs(dft_img[:, :, 0])
        imaginary_part = np.abs(dft_img[:, :, 1])

        # 仅显示幅度谱（通常更常用）
        amplitude_spectrum = np.sqrt(real_part ** 2 + imaginary_part ** 2)
        amplitude_spectrum_shifted = np.fft.fftshift(amplitude_spectrum)

        if crop_size is not None:
            crop_height, crop_width = crop_size
            crop_center = (amplitude_spectrum_shifted.shape[0] // 2, amplitude_spectrum_shifted.shape[1] // 2)  # 中心点坐标

            x_min, x_max = crop_center[1] - crop_width // 2, crop_center[1] + crop_width // 2
            y_min, y_max = crop_center[0] - crop_height // 2, crop_center[0] + crop_height // 2

            cropped_spectrum = amplitude_spectrum_shifted[y_min:y_max, x_min:x_max]

            plt.imshow(cropped_spectrum, cmap='viridis', vmin=0, vmax=np.max(amplitude_spectrum_shifted),
                    extent=(x_min, x_max, y_min, y_max))  # 保持原始坐标范围
        else:
            plt.imshow(amplitude_spectrum_shifted, cmap='viridis', vmin=0, vmax=np.max(amplitude_spectrum_shifted))

        plt.title('Amplitude Spectrum')
        plt.colorbar()
        plt.show()

    def darw_hist(self):
        """
        绘制图像直方图
        """
        self.main_window.camera.stop_thread() # 先关闭实时捕获功能防止图像被覆盖
        self.main_window.basic.reset_image()

        # 获取图像数据
        img = self.main_window.origin_img

        # 检查图像是否为灰度图像
        if len(img.shape) == 3 and img.shape[2] == 3:  # 彩色图像
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 转为灰度图像

        # 计算直方图
        hist, bins = np.histogram(img.flatten(), 256, [0, 256])

        # 绘制直方图
        plt.figure(figsize=(10, 6))
        plt.hist(img.flatten(), bins=bins, color='gray')
        plt.title('Image Histogram')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.xlim([0, 256])
        plt.xticks(np.arange(0, 257, 32))
        plt.yticks(np.arange(0, hist.max() + 1, hist.max() // 10))

        # 显示图形
        plt.show()