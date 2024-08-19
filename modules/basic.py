import sys
from pathlib import Path

import cv2 as cv

from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class Basic:

    def __init__(self, main_window):

        self.main_window = main_window

    def load_image(self):
        """
        加载并显示原始图像。
        """
        self.main_window.camera.stop_thread() # 先关闭实时捕获功能防止图像被覆盖

        # 弹出文件对话框，让用户选择图像
        initial_dir = "samples"  # 可以指定初始目录
        file_filter = "Image files (*.png *.jpg *.jpeg *.bmp)"  # 指定支持的文件类型
        selected_file, _ = QFileDialog.getOpenFileName(self.main_window, "选择图像", initial_dir, file_filter)

        # 如果用户选择了文件，则加载并显示图像
        if selected_file:
            # 将路径转换为Path对象
            self.main_window.image_path = Path(selected_file)
            # 使用 OpenCV 读取图像，并保存为属性
            self.main_window.origin_img = cv.imread(str(self.main_window.image_path))
            # 获取图像的维度信息
            self.main_window.height, self.main_window.width, self.main_window.channels = self.main_window.origin_img.shape
            # 当前处理完成的图像与原始图像相同
            self.main_window.result_img = self.main_window.origin_img
            # 显示原始图像
            self.display_image(self.main_window.result_img)

    def save_image(self):
        """
        保存当前处理完成后的图像。
        """
        self.main_window.camera.stop_thread() # 先关闭实时捕获功能防止图像被覆盖

        # 获取当前处理完成的图像
        img = self.main_window.result_img

        if img is None:
            print("No image to save.")
            return

        # 将图像从 BGR 转换为 RGB 格式以适应 Qt
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # 创建 QImage 并使用图像数据初始化
        qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], QImage.Format_RGB888)
        
        # 从 QImage 创建原始 QPixmap
        pixmap = QPixmap.fromImage(qimg)

        # 弹出保存文件对话框，让用户选择保存位置和文件名
        save_path, _ = QFileDialog.getSaveFileName(
            self.main_window,  # 传递 main_window 作为父窗口
            "保存图像",
            "result.png",
            "PNG Files (*.png)",
            "",  # 添加空字符串作为 selectedFilter 参数
        )
        if not save_path:
            return
        
        # 将QPixmap保存为图像文件
        if not pixmap.save(save_path, "PNG"):
            print(f"Failed to save image to {save_path}")

    def reset_image(self):
        """
        重置图像，恢复到原始状态。
        """
        self.main_window.camera.stop_thread() # 先关闭实时捕获功能防止图像被覆盖

        self.main_window.result_img = self.main_window.origin_img
        self.display_image(self.main_window.result_img)

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
            label = self.main_window.ui.result_img  # 假设 ui.result_img 是正确的 QLabel 名称
            label_width = label.width()
            label_height = label.height()
            
            # 缩放 QPixmap 只按高度缩放
            scaled_pixmap = original_pixmap.scaledToHeight(label_height)
            
            # 设置 QLabel 的对齐方式为居中
            label.setAlignment(Qt.AlignCenter)
            
            # 设置 QPixmap 到 QLabel 中
            label.setPixmap(scaled_pixmap)
            
            # 设置 QLabel 的背景颜色为黑色
            # label.setStyleSheet("background-color: black;")
        else:
            # 如果图像加载失败，打印错误信息
            print("Failed to display image!")
