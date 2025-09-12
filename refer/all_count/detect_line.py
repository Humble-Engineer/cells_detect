import cv2 as cv
import numpy as np
import time
import sys
import os
from collections import deque

class Algorithm:
    """
    算法类，用于处理图像和计数细胞
    """

    def __init__(self, main_window):
        self.main_window = main_window
        self.filter_cells = True

    def detect_type(self):
        self.filter_cells = not self.filter_cells

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
        :return: 轮廓中心点列表和细胞总数
        """
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        num_contours = len(contours)
        
        # 计算每个轮廓的面积
        areas = [cv.contourArea(contour) for contour in contours]

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
        
            print(f"基准单细胞轮廓面积: {median_smallest_10_percent_area}")

        outline_counts = len(filtered_contours)
        
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
        
        # 存储细胞中心点
        cell_centers = []
        
        for index, (selected_contour, cell_count) in enumerate(zip(filtered_contours, estimated_cell_counts)):
            # 根据细胞数量选择颜色
            color = (0, 0, 255) if cell_count > 1 else (255, 0, 0)
            cv.drawContours(img, [selected_contour], -1, color, thickness=max(1, int(img.shape[0] / 500)))  # 根据图像高度调整轮廓线粗细
            center, radius = cv.minEnclosingCircle(selected_contour)
            center = tuple(map(int, center))
            radius = int(radius)
            
            # 添加中心点和半径到列表
            cell_centers.append((center, radius, selected_contour))
            
            if cell_count > 1:
                text = f"{cell_count}"
                text_x = center[0] - radius
                text_y = center[1] - radius
                # 根据图像尺寸调整文字位置和大小
                self.draw_text(img, text, (text_x, text_y), font_color=(0, 0, 255))

        # 绘制找到的细胞总数
        self.draw_cells_found_text(img, total_cells)
        
        return total_cells, outline_counts, cell_centers

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
            if not (x < self.main_window.border_distance or y < self.main_window.border_distance or 
                    x + w > img.shape[1] - self.main_window.border_distance or 
                    y + h > img.shape[0] - self.main_window.border_distance):
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
            mask = cv.dilate(mask, kernel, iterations=self.main_window.dilate_times)
            mask = cv.erode(mask, kernel, iterations=self.main_window.erode_times)
            
            # 增加开运算去除小噪点
            mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)

            total_cells, outline_counts, cell_centers = self.find_and_draw_contours(mask, img, self.filter_cells) # 启用细胞团检测

            fps_text, _ = self.calculate_fps_text(start_time)

            self.draw_text(img, fps_text, (int(img.shape[1]*0.03), int(img.shape[0]*0.06)))

            self.main_window.result_img = img
            self.main_window.basic.display_image(img)

            self.main_window.mat.add_data(total_cells)
            
            try:
                # 如果被设置为记录模式就记录数据
                if self.main_window.handler.record_mode:    
                    self.main_window.handler.write_to_file(f"{total_cells}\n", mode='a')
            except:
                print("An error occurred during writing to file.")
                
        except Exception as e:
            print(f"An error occurred during image processing: {e}")

class VideoCellCounter:
    """
    处理视频并计算整个视频中出现的细胞总数（基于检测线穿越计数）
    """
    
    def __init__(self):
        # 创建模拟的主窗口对象
        self.mock_main_window = self.create_mock_main_window()
        
        # 初始化算法模块
        self.algorithm = Algorithm(self.mock_main_window)
        
        # 设置跟踪参数
        self.min_area = 20      # 减小最小细胞面积阈值
        self.detection_line_x = None  # 检测线的x坐标（将在第一帧中设置）
        
        # 跟踪数据
        self.tracked_cells = {}  # {cell_id: {'contour': contour, 'centroid_history': [(x,y), ...], 'has_crossed': bool}}
        self.next_cell_id = 0
        self.total_count = 0  # 总计数
        
    def create_mock_main_window(self):
        """
        创建模拟的主窗口对象，包含算法所需的所有参数
        """
        mock_window = type('MockMainWindow', (), {})()
        
        # 设置默认参数，与main.py中一致
        mock_window.H_min = 30
        mock_window.H_max = 90
        mock_window.S_min = 70
        mock_window.S_max = 255
        mock_window.V_min = 70
        mock_window.V_max = 255
        
        mock_window.gauss_shape = 5
        mock_window.struct_shape = 3
        mock_window.erode_times = 1
        mock_window.dilate_times = 1
        
        mock_window.low_percentage = 0.4
        mock_window.growth_factor = 1.75
        mock_window.border_distance = 10
        
        # 模拟其他必需的组件
        mock_window.basic = type('Basic', (), {})()
        mock_window.basic.display_image = lambda img: None
        
        mock_window.mat = type('Mat', (), {})()
        mock_window.mat.add_data = lambda data: None
        
        mock_window.handler = type('Handler', (), {})()
        mock_window.handler.record_mode = False
        mock_window.handler.write_to_file = lambda data, mode: None
        
        return mock_window

    def extract_cell_contours(self, frame):
        """
        从帧中提取细胞轮廓
        
        :param frame: 输入帧
        :return: 细胞轮廓列表
        """
        # 保存原始图像
        self.mock_main_window.origin_img = frame.copy()
        
        # 设置HSV范围
        lower_hsv = np.array([self.mock_main_window.H_min, 
                              self.mock_main_window.S_min, 
                              self.mock_main_window.V_min])
        upper_hsv = np.array([self.mock_main_window.H_max, 
                              self.mock_main_window.S_max, 
                              self.mock_main_window.V_max])
        
        try:
            # 图像处理流程
            img = cv.resize(frame, (0, 0), fx=1, fy=1)
            img = cv.GaussianBlur(img, 
                                  (self.mock_main_window.gauss_shape, 
                                   self.mock_main_window.gauss_shape), 0)
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
            
            # 形态学操作
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, 
                                              (self.mock_main_window.struct_shape, 
                                               self.mock_main_window.struct_shape))
            mask = cv.dilate(mask, kernel, iterations=self.mock_main_window.dilate_times)
            mask = cv.erode(mask, kernel, iterations=self.mock_main_window.erode_times)
            mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
            
            # 查找轮廓
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            
            # 过滤太小的轮廓
            filtered_contours = []
            for contour in contours:
                area = cv.contourArea(contour)
                if area > self.min_area:
                    filtered_contours.append(contour)
            
            return filtered_contours
            
        except Exception as e:
            print(f"处理帧时出错: {e}")
            return []

    def get_contour_centroid(self, contour):
        """
        获取轮廓质心（重心）
        
        :param contour: 轮廓
        :return: 质心坐标 (x, y)
        """
        moments = cv.moments(contour)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            return (cx, cy)
        else:
            # 使用边界矩形中心作为备选
            x, y, w, h = cv.boundingRect(contour)
            return (x + w//2, y + h//2)

    def match_contours(self, prev_contours_with_data, curr_contours):
        """
        匹配前后帧中的轮廓
        
        :param prev_contours_with_data: 前一帧的轮廓和数据 [(contour, data), ...]
        :param curr_contours: 当前帧的轮廓
        :return: 匹配对列表 [(prev_idx, curr_idx), ...] 和未匹配的轮廓索引
        """
        if not prev_contours_with_data or not curr_contours:
            return [], list(range(len(curr_contours)))
        
        matched_pairs = []
        used_curr = set()
        
        # 对于每个前一帧的轮廓，寻找最近的当前帧轮廓
        for prev_idx, (prev_contour, prev_data) in enumerate(prev_contours_with_data):
            # 获取前一帧质心
            prev_centroid = self.get_contour_centroid(prev_contour)
            best_match_idx = -1
            best_distance = float('inf')
            
            # 寻找最近的当前帧轮廓
            for curr_idx, curr_contour in enumerate(curr_contours):
                if curr_idx in used_curr:
                    continue
                    
                curr_centroid = self.get_contour_centroid(curr_contour)
                distance = np.sqrt((prev_centroid[0] - curr_centroid[0])**2 + 
                                 (prev_centroid[1] - curr_centroid[1])**2)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match_idx = curr_idx
            
            # 如果找到了匹配（距离不能太远）
            if best_match_idx != -1 and best_distance < 100:  # 最大移动距离阈值
                matched_pairs.append((prev_idx, best_match_idx))
                used_curr.add(best_match_idx)
        
        # 未匹配的当前帧轮廓
        unmatched_curr = [i for i in range(len(curr_contours)) if i not in used_curr]
        
        return matched_pairs, unmatched_curr

    def update_cell_tracking(self, curr_contours):
        """
        更新细胞跟踪状态
        
        :param curr_contours: 当前帧的轮廓列表
        :return: 更新后的跟踪细胞字典
        """
        if not curr_contours:
            return {}
        
        # 获取前一帧的轮廓和数据
        prev_contours_with_data = [(data['contour'], data) for data in self.tracked_cells.values()]
        prev_ids = list(self.tracked_cells.keys())
        
        if not prev_contours_with_data:
            # 第一帧或重新开始，所有轮廓都是新细胞
            new_tracked_cells = {}
            for i, contour in enumerate(curr_contours):
                centroid = self.get_contour_centroid(contour)
                new_tracked_cells[self.next_cell_id] = {
                    'contour': contour,
                    'centroid_history': [centroid],  # 记录质心历史
                    'has_crossed': False  # 是否已穿过检测线
                }
                self.next_cell_id += 1
            return new_tracked_cells
        
        # 匹配前后帧轮廓
        matched_pairs, unmatched_curr = self.match_contours(prev_contours_with_data, curr_contours)
        
        # 更新匹配的细胞
        updated_tracked_cells = {}
        for prev_idx, curr_idx in matched_pairs:
            prev_id = prev_ids[prev_idx]
            contour = curr_contours[curr_idx]
            centroid = self.get_contour_centroid(contour)
            
            if prev_id in self.tracked_cells:
                cell_data = self.tracked_cells[prev_id].copy()
                cell_data['contour'] = contour
                # 更新质心历史（保留最近几个位置）
                cell_data['centroid_history'].append(centroid)
                if len(cell_data['centroid_history']) > 10:  # 只保留最近10个位置
                    cell_data['centroid_history'] = cell_data['centroid_history'][-10:]
                updated_tracked_cells[prev_id] = cell_data
        
        # 添加新的未匹配细胞
        for curr_idx in unmatched_curr:
            contour = curr_contours[curr_idx]
            centroid = self.get_contour_centroid(contour)
            updated_tracked_cells[self.next_cell_id] = {
                'contour': contour,
                'centroid_history': [centroid],
                'has_crossed': False
            }
            self.next_cell_id += 1
        
        return updated_tracked_cells

    def check_crossing_detection_line(self, tracked_cells, frame_display):
        """
        检查细胞是否穿过检测线（基于质心位置）
        
        :param tracked_cells: 当前跟踪的细胞
        :param frame_display: 用于显示的帧
        :return: 更新后的跟踪细胞字典
        """
        new_total_count = self.total_count
        
        for cell_id, cell_data in tracked_cells.items():
            centroid_history = cell_data['centroid_history']
            has_crossed = cell_data['has_crossed']
            
            # 只有当有足够历史记录时才检查穿越
            if len(centroid_history) >= 2 and not has_crossed:
                prev_centroid = centroid_history[-2]
                curr_centroid = centroid_history[-1]
                
                # 检查是否从右到左穿过检测线
                if prev_centroid[0] > self.detection_line_x and curr_centroid[0] <= self.detection_line_x:
                    # 质心从右到左穿过检测线
                    cell_data['has_crossed'] = True
                    new_total_count += 1
                    print(f"细胞 {cell_id} 的质心穿过检测线，总计数: {new_total_count}")
                    
                    # 在图像上标记已计数的细胞
                    cv.circle(frame_display, curr_centroid, 5, (0, 0, 255), -1)  # 红色点标记
            
            # 绘制轮廓和质心
            contour = cell_data['contour']
            if len(centroid_history) > 0:
                current_centroid = centroid_history[-1]
                # 绘制轮廓
                cv.drawContours(frame_display, [contour], -1, (0, 255, 0), 2)
                # 绘制质心
                cv.circle(frame_display, current_centroid, 3, (255, 0, 0), -1)
                # 绘制细胞ID
                cv.putText(frame_display, f"{cell_id}", 
                          (current_centroid[0]-10, current_centroid[1]-10), 
                          cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # 绘制轨迹
                if len(centroid_history) > 1:
                    for i in range(1, len(centroid_history)):
                        cv.line(frame_display, centroid_history[i-1], centroid_history[i], (255, 255, 0), 1)
        
        # 更新总计数
        self.total_count = new_total_count
        
        return tracked_cells

    def process_video(self, video_path, show_progress=True):
        """
        处理视频并计算细胞总数（基于检测线穿越）
        
        :param video_path: 视频文件路径
        :param show_progress: 是否显示进度
        :return: 视频中出现的细胞总数
        """
        # 打开视频文件
        cap = cv.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        # 获取视频信息
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        
        # 设置检测线位置（图像中间）
        self.detection_line_x = width // 2  # 位于图像中间位置
        
        # 创建用于显示的窗口
        cv.namedWindow('Cell Tracking', cv.WINDOW_NORMAL)
        cv.resizeWindow('Cell Tracking', min(1200, width), min(800, height))
        
        frame_count = 0
        
        # 获取总帧数用于进度显示
        total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        
        print(f"开始处理视频，共 {total_frames} 帧...")
        print(f"检测线位置: x = {self.detection_line_x}")
        print("使用质心穿越检测线进行计数")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # 在帧上绘制检测线
            frame_display = frame.copy()
            cv.line(frame_display, (self.detection_line_x, 0), 
                   (self.detection_line_x, height), (0, 255, 0), 2)
            
            # 提取当前帧的细胞轮廓
            curr_contours = self.extract_cell_contours(frame)
            
            # 更新细胞跟踪
            updated_tracked_cells = self.update_cell_tracking(curr_contours)
            
            # 检查细胞是否穿过检测线
            self.tracked_cells = self.check_crossing_detection_line(updated_tracked_cells, frame_display)
            
            # 显示当前帧信息
            cv.putText(frame_display, f"Frame: {frame_count}/{total_frames}", (10, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.putText(frame_display, f"Total Count: {self.total_count}", (10, 70), 
                      cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame_display, f"Tracked Cells: {len(self.tracked_cells)}", (10, 110), 
                      cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            # 显示处理后的帧
            cv.imshow('Cell Tracking', frame_display)
            
            # 按'q'键退出，按空格键暂停
            key = cv.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                cv.waitKey(0)  # 按任意键继续
            
            # 显示进度
            if show_progress and frame_count % 10 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"处理进度: {progress:.1f}% ({frame_count}/{total_frames} 帧)，当前计数: {self.total_count}")
        
        # 释放视频资源
        cap.release()
        cv.destroyAllWindows()
        
        print(f"视频处理完成，共处理 {frame_count} 帧")
        print(f"最终细胞计数: {self.total_count}")
        
        return self.total_count

def main():
    """
    主函数
    """
    # 创建细胞计数器
    counter = VideoCellCounter()
    
    # 使用指定的测试视频
    video_path = os.path.join("refer", "all_count", "t3.mp4")
    
    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"错误: 找不到测试视频文件 '{video_path}'")
        # 尝试让用户输入路径
        video_path = input("请输入视频文件路径: ").strip()
        if not os.path.exists(video_path):
            print(f"错误: 找不到文件 '{video_path}'")
            return
    
    try:
        # 处理视频并计算细胞总数
        print("正在处理视频，请稍候...")
        print("提示: 按 'q' 键退出，按空格键暂停/继续")
        total_cells = counter.process_video(video_path)
        
        print("\n" + "="*50)
        print(f"视频处理完成！")
        print(f"整个视频中穿过检测线的细胞总数为: {total_cells}")
        print("="*50)
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main()