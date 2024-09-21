import cv2 as cv
import numpy as np
import time


class Algorithm:

    def __init__(self, main_window):

        self.main_window = main_window

    def calculate_fps_text(self, start_time):
            """
            计算FPS并返回FPS文本和运行时间
            """
            # 计算运行时间
            run_time = time.perf_counter() - start_time
            fps_text = f"FPS:{int(1/run_time)} Time:{int(1000*run_time)}ms"
            return fps_text, run_time
    
    def draw_text(self, img, text, position, font_scale=None, font_thickness=None, font_color=(255, 255, 255)):
        """
        在图像上绘制文字。
        
        :param img: 图像
        :param text: 要绘制的文字
        :param position: 文字的位置 (x, y)
        :param font_scale: 字体大小
        :param font_thickness: 字体厚度
        :param font_color: 字体颜色 (B, G, R)
        """
        if font_scale is None:
            font_scale = img.shape[0] / 1000  # 根据图像的高度调整字体大小
        if font_thickness is None:
            font_thickness = max(1, int(3*font_scale))  # 确保至少有1的厚度
        font = cv.FONT_HERSHEY_SIMPLEX
        text_x, text_y = position
        cv.putText(img, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

    def draw_cells_found_text(self, img, total_cells):
        """
        在图像底部左角绘制找到的细胞总数。
        
        :param img: 图像
        :param total_cells: 找到的细胞总数
        """
        text = f"Total cells found: {total_cells}"
        # 计算左下角的位置
        text_x = int(img.shape[1] * 0.03)  # 距离左边3%
        text_y = int(img.shape[0] * 0.90)  # 距离底边3%
        self.draw_text(img, text, (text_x, text_y))
        
        # 计算细胞浓度
        cell_concent = round(total_cells / 6, 2)
        
        text = f"Concentration: {cell_concent} w/ml"
        text_x = int(img.shape[1] * 0.03)  # 距离左边3%
        text_y = int(img.shape[0] * 0.95)  # 距离底边3%
        self.draw_text(img, text, (text_x, text_y))

        

    def find_and_draw_contours(self, mask, img, filter_cells=True):
        """
        查找轮廓并在图像上绘制。
        
        :param mask: 二值掩膜图像
        :param img: 原始图像
        :param filter_cells: 是否启用过滤边缘细胞和估计细胞团数量
        """
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        num_contours = len(contours)
        
        # 计算每个轮廓的面积
        areas = [cv.contourArea(contour) for contour in contours]

        # if filter_cells:
        #     # 过滤靠近图像边界的轮廓
        #     filtered_contours, filtered_areas = self.filter_border_contours(contours, areas, img)
        
        # else:
        # 如果不启用过滤，则直接使用原始轮廓和面积
        filtered_contours = contours
        filtered_areas = areas
        
        # 排序过滤后的面积
        sorted_areas = sorted(filtered_areas)
        
        if filter_cells:
            # 找到最小10%面积的阈值索引
            threshold_index = int(len(sorted_areas) * self.main_window.low_percentage)

            # 如果轮廓太少，设置最小轮廓作为参考
            if threshold_index == 0:
                threshold_index = 1

            # 取最小10%的面积
            smallest_10_percent_areas = sorted_areas[:threshold_index]
        
            # 计算最小10%面积的中位数
            # 检查列表是否为空以避免越界
            if smallest_10_percent_areas:
                median_smallest_10_percent_area = smallest_10_percent_areas[len(smallest_10_percent_areas) // 2]
            else:
                median_smallest_10_percent_area = 0
        
        if filter_cells:
            # 估计每个轮廓代表的细胞数量
            estimated_cell_counts = []
            for area in filtered_areas:
                cell_count = 1
                while area > median_smallest_10_percent_area * (self.main_window.growth_factor * cell_count):
                    cell_count += 1
                estimated_cell_counts.append(cell_count)
            
            total_cells = sum(estimated_cell_counts)
        else:
            # 如果不启用估计，则所有轮廓默认为单个细胞
            estimated_cell_counts = [1] * len(filtered_contours)
            total_cells = len(filtered_contours)
        
        for index, (selected_contour, cell_count) in enumerate(zip(filtered_contours, estimated_cell_counts)):
            cv.drawContours(img, filtered_contours, index, (255, 0, 0), thickness=max(1, int(img.shape[0] / 300)))  # 根据图像高度调整轮廓线粗细
            center, radius = cv.minEnclosingCircle(selected_contour)
            center = tuple(map(int, center))
            radius = int(radius)
            if cell_count > 1:
                text = f"{cell_count}"
                text_x = center[0] - radius
                text_y = center[1] - radius
                # 根据图像尺寸调整文字位置和大小
                self.draw_text(img, text, (text_x, text_y), font_color=(0, 0, 255))

        # 绘制找到的细胞总数
        self.draw_cells_found_text(img, total_cells)
        
        # 输出或使用最小10%轮廓面积的中位数
        # print(f"最小10%轮廓面积的中位数: {median_smallest_10_percent_area:.2f} 像素")
        
        return total_cells
    
    def filter_border_contours(self, contours, areas, img):
        """
        过滤靠近图像边界的轮廓。
        
        :param contours: 轮廓列表
        :param areas: 轮廓对应的面积列表
        :param img: 原始图像
        :return: 过滤后的轮廓和面积列表
        """
        filtered_contours = []
        filtered_areas = []
        for contour, area in zip(contours, areas):
            # 检查轮廓是否靠近边界
            x, y, w, h = cv.boundingRect(contour)
            if not (x < self.main_window.border_distance or y < self.main_window.border_distance or x + w > img.shape[1] - self.main_window.border_distance or y + h > img.shape[0] - self.main_window.border_distance):
                filtered_contours.append(contour)
                filtered_areas.append(area)
        return filtered_contours, filtered_areas

    def count(self):
        start_time = time.perf_counter()

        time.sleep(0.02)

        lower_hsv = np.array([self.main_window.H_min, self.main_window.S_min, self.main_window.V_min])
        upper_hsv = np.array([self.main_window.H_max, self.main_window.S_max, self.main_window.V_max])

        try:
            # Resize image for processing
            img = cv.resize(self.main_window.origin_img, (0,0), fx=1, fy=1)
            # 高斯模糊(卷积核越大,可去除更多噪声,但会损失更多细节)
            img = cv.GaussianBlur(img, (self.main_window.gauss_shape, self.main_window.gauss_shape), 0)
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)

            # 使用结构元素(卷积核大小作用类似)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (self.main_window.struct_shape,self.main_window.struct_shape))
            # 形态学操作(可选迭代次数)
            mask = cv.erode(mask, kernel, iterations=self.main_window.erode_times)
            mask = cv.dilate(mask, kernel, iterations=self.main_window.dilate_times)

            total_cells = self.find_and_draw_contours(mask, img, filter_cells=True) # 启用细胞团检测

            fps_text, _ = self.calculate_fps_text(start_time)

            self.draw_text(img, fps_text, (int(img.shape[1]*0.03), int(img.shape[0]*0.06)))

            self.main_window.result_img = img
            self.main_window.basic.display_image(img)

            self.main_window.mat.add_data(total_cells)

            # 打印使用的参数
            # print(f"H:({self.H_min},{self.H_max}),S:({self.S_min},{self.S_max}),V:({self.V_min},{self.V_max})\n"
            #       f"gauss_shape={self.gauss_shape}, struct_shape={self.struct_shape},\n"
            #       f"erode_times={self.erode_times}, dilate_times={self.dilate_times}")

        except Exception as e:
            print(f"An error occurred during image processing: {e}")

