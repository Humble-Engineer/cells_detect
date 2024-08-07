'''
打包发布命令：
pyinstaller -F main.py
-w (–windowed / –noconsole): 对于 GUI 应用程序，隐藏控制台窗口。
--icon=FILE.ico: 指定可执行文件的图标。

'''

import sys
from pathlib import Path

import cv2 as cv
import time
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from MainWindow_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    """
    主窗口类，用于显示图像。
    """
    def __init__(self):
        """
        初始化主窗口，创建图像显示标签并加载显示用户选择的图像。
        """
        super().__init__()  # 调用父类构造函数

        self.ui = Ui_MainWindow()  # 实例化UI类
        self.ui.setupUi(self)  # 使用UI类的实例设置主窗口的界面
        
        self.slot_bind()  # 调用band方法进行进一步的初始化或设置
        
        self.argu_init()
        
    def slot_bind(self):
        """
        绑定按钮或菜单项的点击事件到相应的函数。
        """
        # self.ui.___MENU___.triggered.connect(___FUNCTION___)
        # self.ui.___ACTION___.triggered.connect(___FUNCTION___)
        # self.ui.___BUTTON___.clicked.connect(___FUNCTION___)
        # self.ui.___COMBO_BOX___.currentIndexChanged.connect(___FUNCTION___)
        # self.ui.___SPIN_BOX___.valueChanged.connect(___FUNCTION___)
        # 自定义信号.属性名.connect(___FUNCTION___)

        # 绑定加载图像按钮的点击事件
        self.ui.load_button.clicked.connect(self.load_image)
        # 绑定保存图像按钮的点击事件
        self.ui.save_button.clicked.connect(self.save_image)
        # 绑定重置图像按钮的点击事件
        self.ui.reset_button.clicked.connect(self.reset_image)

        # 绑定图像直方图按钮的点击事件
        self.ui.draw_button.clicked.connect(self.darw_hist)
        # 绑定傅里叶变换按钮的点击事件
        self.ui.fft_button.clicked.connect(self.fast_fft)

        # 绑定默认参数按钮的点击事件
        self.ui.default_button.clicked.connect(self.argu_init)
        # 绑定计数按钮的点击事件
        self.ui.count_button.clicked.connect(self.count)


        self.sliders = [self.ui.H_min_Slider, self.ui.H_max_Slider, self.ui.S_min_Slider,
                        self.ui.S_max_Slider, self.ui.V_min_Slider, self.ui.V_max_Slider,

                        self.ui.Gauss_Slider, self.ui.Struct_Slider, 
                        self.ui.Erode_Slider, self.ui.Dilate_Slider]
        
        for slider in self.sliders:
            slider.sliderReleased.connect(self.argu_update)
            slider.sliderMoved.connect(self.argu_update)
            slider.valueChanged.connect(self.argu_update)



    def argu_init(self):

        self.ui.H_min_Slider.setValue(20)
        self.ui.H_max_Slider.setValue(80)
        self.ui.S_min_Slider.setValue(30)
        self.ui.S_max_Slider.setValue(255)
        self.ui.V_min_Slider.setValue(30)
        self.ui.V_max_Slider.setValue(255)

        self.ui.Gauss_Slider.setValue(1)
        self.ui.Struct_Slider.setValue(2)
        self.ui.Erode_Slider.setValue(1)
        self.ui.Dilate_Slider.setValue(1)

        self.argu_update()

        print("检测参数已经重置...")

    def argu_update(self):

        self.H_min = self.ui.H_min_Slider.value()
        self.H_max = self.ui.H_max_Slider.value()
        self.S_min = self.ui.S_min_Slider.value()
        self.S_max = self.ui.S_max_Slider.value()
        self.V_min = self.ui.V_min_Slider.value()
        self.V_max = self.ui.V_max_Slider.value()

        self.ui.H_min_label.setText(str(self.H_min))
        self.ui.H_max_label.setText(str(self.H_max))
        self.ui.S_min_label.setText(str(self.S_min))
        self.ui.S_max_label.setText(str(self.S_max))
        self.ui.V_min_label.setText(str(self.V_min))
        self.ui.V_max_label.setText(str(self.V_max))

        self.gauss_shape = 2*self.ui.Gauss_Slider.value()+1
        self.struct_shape = 2*self.ui.Struct_Slider.value()+1
        self.erode_times = 2*self.ui.Erode_Slider.value()+1
        self.dilate_times = 2*self.ui.Dilate_Slider.value()+1

        self.ui.Gauss_label.setText(str(self.gauss_shape))
        self.ui.Struct_label.setText(str(self.struct_shape))
        self.ui.Erode_label.setText(str(self.erode_times))
        self.ui.Dilate_label.setText(str(self.dilate_times))

    def load_image(self):
        """
        加载并显示原始图像。
        """
        # 弹出文件对话框，让用户选择图像
        initial_dir = "samples"  # 可以指定初始目录
        file_filter = "Image files (*.png *.jpg *.jpeg *.bmp)"  # 指定支持的文件类型
        selected_file, _ = QFileDialog.getOpenFileName(self, "选择图像", initial_dir, file_filter)

        # 如果用户选择了文件，则加载并显示图像
        if selected_file:
            # 将路径转换为Path对象
            self.image_path = Path(selected_file)
            # 使用 OpenCV 读取图像，并保存为属性
            self.origin_img = cv.imread(str(self.image_path))
            # 获取图像的维度信息
            self.height, self.width, self.channels = self.origin_img.shape
            # 当前处理完成的图像与原始图像相同
            self.result_img = self.origin_img
            # 显示原始图像
            self.display_image(self.result_img)

    def save_image(self):
        """
        保存当前处理完成后的图像。
        """
        # 获取当前显示的QPixmap
        current_pixmap = self.ui.result_img.pixmap()

        if current_pixmap.isNull():
            print("No image to save.")
            return

        # 弹出保存文件对话框，让用户选择保存位置和文件名
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图像",
            "result.png",
            "PNG Files (*.png)"
        )

        if not save_path:
            return

        # 将QPixmap保存为图像文件
        if not current_pixmap.save(save_path, "PNG"):
            print(f"Failed to save image to {save_path}")

    def reset_image(self):
        """
        重置图像，恢复到原始状态。
        """
        self.result_img = self.origin_img
        self.display_image(self.result_img)

    def display_image(self, img):
        """
        显示传入的图像
        :param img: 需要显示的图像，应为numpy数组格式
        """
        if img is not None:
            # 将图像从 BGR 转换为 RGB 格式以适应 Qt
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

            # 创建 QImage 并使用图像数据初始化
            qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], QImage.Format_RGB888)

            # 从 QImage 创建原始 QPixmap
            original_pixmap = QPixmap.fromImage(qimg)

            # 获取 QLabel 的尺寸
            label_width = self.ui.result_img.width()
            label_height = self.ui.result_img.height()

            # 缩放 QPixmap 只按高度缩放
            scaled_pixmap = original_pixmap.scaledToHeight(label_height)
            
            # 设置 QLabel 的对齐方式为居中
            self.ui.result_img.setAlignment(Qt.AlignCenter)

            # 设置 QPixmap 到 QLabel 中
            self.ui.result_img.setPixmap(scaled_pixmap)

            # 设置 QLabel 的背景颜色为黑色
            self.ui.result_img.setStyleSheet("background-color: black;")

        else:
            # 如果图像加载失败，打印错误信息
            print("Failed to display image!")

    def darw_hist(self):
        """
        绘制图像直方图
        """
        self.reset_image()
        # 获取图像数据
        img = self.origin_img

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

    def fast_fft(self):
        """
        使用OpenCV对给定的图像进行傅里叶变换（快速傅里叶变换），并使用matplotlib显示频谱图像。
        可选地，可以指定裁剪大小来放大显示幅度谱的中间部分。

        参数:
            image (numpy.ndarray): 输入图像，应为二维灰度图像或三维彩色图像（BGR顺序）
            crop_size (tuple, optional): 裁剪区域的大小，格式为 (height, width)，默认为 None（不裁剪）
        """
        self.reset_image()
        self.result_img = cv.cvtColor(self.result_img, cv.COLOR_BGR2GRAY)

        # 确保图像为浮点类型，便于进行数学运算
        image_float = self.result_img.astype(np.float32)

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

    def calculate_fps_text(self, start_time):
            run_time = time.perf_counter() - start_time
            fps_text = f"FPS:{int(1/run_time)} Time:{int(1000*run_time)}ms"
            return fps_text, run_time

    def draw_text(self, img, text, position, font_scale=None, font_thickness=None, font_color=(255, 255, 255)):
        if font_scale is None:
            font_scale = img.shape[0] / 1000  # Adjust based on the height of the image
        if font_thickness is None:
            font_thickness = max(1, int(3*font_scale))  # Ensure at least a thickness of 1
        font = cv.FONT_HERSHEY_SIMPLEX
        text_x, text_y = position
        cv.putText(img, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

    def draw_cells_found_text(self, img, num_contours):
        text = f"Cells have been found: {num_contours}"
        # Calculate the position for the left bottom corner
        text_x = int(img.shape[1] * 0.03)  # 3% from the left side
        text_y = int(img.shape[0] * 0.97)  # 3% from the bottom
        self.draw_text(img, text, (text_x, text_y))

    def find_and_draw_contours(self, mask, img):
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        num_contours = len(contours)
        for index, selected_contour in enumerate(contours):
            cv.drawContours(img, contours, index, (255, 0, 0), thickness=max(1, int(img.shape[0] / 300)))  # Adjust thickness based on image height
            center, radius = cv.minEnclosingCircle(selected_contour)
            center = tuple(map(int, center))
            radius = int(radius)
            text = str(index + 1)
            text_x = center[0] - radius
            text_y = center[1] - radius
            # Adjust text position and size based on the image dimensions
            self.draw_text(img, text, (text_x, text_y), font_color=(0, 0, 255))

        # Draw the number of cells found text
        self.draw_cells_found_text(img, num_contours)

    def count(self):
        start_time = time.perf_counter()

        # time.sleep(0.1)

        lower_hsv = np.array([self.H_min, self.S_min, self.V_min])
        upper_hsv = np.array([self.H_max, self.S_max, self.V_max])

        try:
            # Resize image for processing
            img = cv.resize(self.origin_img, (0,0), fx=1, fy=1)
            # 高斯模糊(卷积核越大,可去除更多噪声,但会损失更多细节)
            img = cv.GaussianBlur(img, (self.gauss_shape, self.gauss_shape), 0)
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)

            # 使用结构元素(卷积核大小作用类似)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (self.struct_shape,self.struct_shape))
            # 形态学操作(可选迭代次数)
            mask = cv.erode(mask, kernel, iterations=self.erode_times) #腐蚀
            mask = cv.dilate(mask, kernel, iterations=self.dilate_times) #膨胀

            self.find_and_draw_contours(mask, img)

            fps_text, _ = self.calculate_fps_text(start_time)
            # Adjust FPS text position and size based on the image dimensions
            self.draw_text(img, fps_text, (int(img.shape[1]*0.03), int(img.shape[0]*0.06)))

            self.result_img = img
            self.display_image(img)

            # 打印使用的参数
            print(f" H_min={self.H_min}, S_min={self.S_min}, V_min={self.V_min}, "
                f"H_max={self.H_max}, S_max={self.S_max}, V_max={self.V_max}, "
                f"gauss_shape={self.gauss_shape}, struct_shape={self.struct_shape}, "
                f"erode_times={self.erode_times}, dilate_times={self.dilate_times}")

        except Exception as e:
            print(f"An error occurred during image processing: {e}")


if __name__ == "__main__":
    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 创建主窗口并显示
    main_window = MainWindow()
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec())