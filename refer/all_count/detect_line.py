import cv2 as cv
import numpy as np
import time
import os

# ---------------------------------------------------------------------------
# 左侧说明文字（HUD）自适应排版参数
# ---------------------------------------------------------------------------
HUD_FONT = cv.FONT_HERSHEY_SIMPLEX
HUD_X_RATIO = 0.03             # 左边距占图像宽度的比例
HUD_BLOCK_HEIGHT_RATIO = 0.25  # 【核心】几行说明文字整块高度 ≈ 整图高度 × 0.25
HUD_LINE_FILL = 0.53           # 字号 = 行距 × 该系数（标定值：720p 下与原来的 fontScale=1 观感一致）
HUD_FIRST_BASELINE = 1.05      # 首行基线 = 行距 × 该系数（给首行留上边距，避免贴顶被裁）
HUD_LINES_PAD = 0.3            # 行距 = 整块高度 ÷ (行数 + 该余量)，余量留给首行上边距和末行降部
HUD_WIDTH_LIMIT = 0.94         # 文字最宽不超过图像宽度的 94%，竖屏/窄幅视频防出画

# ---------------------------------------------------------------------------
# 编号找回（"合并后又分离"的细胞）参数
# ---------------------------------------------------------------------------
REID_NEAR_LEFT_RATIO = 0.05    # 消失前中心在左侧 5% 宽度内 = 正常流出可视区域，不参与找回
REID_RIGHT_RATIO = 0.05        # 轮廓右边距图宽 5% 以内 = 贴右边界（新细胞只可能从这里进来）
REID_ADJACENT_FACTOR = 1.8     # 新轮廓与宿主中心距 ≤ 该系数 × 两者平均尺寸 = "贴在一起"
REID_MAX_FRAMES = 200          # 待找回记录的最长等待帧数（宿主一直在场上才有效）
REID_MAX_LOST_DIST_RATIO = 1.0   # 归还时新轮廓离"消亡位置"的最远允许距离（占图宽比例）
                                 # 默认 1.0 = 基本不设限：因为"中部冒出的轮廓绝不允许发新号"，
                                 # 宁可认最近的暂存编号；若发现误认领可调小（如 0.5、0.35）

# ---------------------------------------------------------------------------
# 帧间匹配参数
# ---------------------------------------------------------------------------
MATCH_MAX_DISTANCE = 100       # 相邻帧同一细胞的最大移动距离（像素），超过就不算同一个细胞

# ---------------------------------------------------------------------------
# 轮廓提取参数
# ---------------------------------------------------------------------------
PRE_ERODE_TIMES = 1            # HSV 掩膜在后续形态学处理（膨胀/腐蚀/开运算）之前，
                               # 先腐蚀的次数：把刚好接触的两个细胞之间那点细连接蚀断，
                               # 减少轮廓粘成一团（改 0 即恢复原来的流程）


def hud_text_layout(width, height, lines, block_ratio=HUD_BLOCK_HEIGHT_RATIO,
                    x_ratio=HUD_X_RATIO, line_fill=HUD_LINE_FILL, font=HUD_FONT):
    """
    按整张图的尺寸，算出左侧说明文字的字号 / 字粗 / 行距 / 起始位置。

    - 整块文字（首行上边距 → 末行降部）高度恒约为图高的 block_ratio（默认 1/4）：
      行距 = 图高 × block_ratio ÷ (行数 + 余量)，所以图变大字号跟着变大、图变小跟着变小；
    - 字号 = 行距 × HUD_LINE_FILL，再用 cv.getTextSize 实测的 fontScale=1 参考字高换算
      （不写死像素数字，换字体也只需改 HUD_FONT / 系数）；
    - 字粗（thickness）跟着字号线性走：字越大越粗，小图也不会细到看不清；
    - 若最宽一行超过图宽的 HUD_WIDTH_LIMIT，按比例缩小字号，保证文字不出画。

    :param width: 图像宽度（像素）
    :param height: 图像高度（像素）
    :param lines: 要画的几行文字列表
    :return: dict(font_scale, thickness, step, x, ys, block_px)
    """
    n = max(1, len(lines))
    block_px = max(1.0, height * block_ratio)              # 整块文字占的高度
    step = block_px / (n + HUD_LINES_PAD)                  # 行距（基线间距）

    # fontScale=1 时一行的参考字高，用它把"目标字高"换算成 fontScale
    ref_h = cv.getTextSize('Frame 0/0', font, 1.0, 1)[0][1] or 22.0

    font_scale = max(0.3, step * line_fill / ref_h)
    thickness = max(1, int(round(font_scale * 2)))

    # 太宽就等比缩小（竖屏视频宽度小，只靠高度定字号会出画）
    max_w = width * HUD_WIDTH_LIMIT
    for _ in range(3):
        widest = max(cv.getTextSize(t, font, font_scale, thickness)[0][0] for t in lines)
        if widest <= max_w:
            break
        font_scale *= max_w / widest
        thickness = max(1, int(round(font_scale * 2)))

    x = int(max(4, width * x_ratio))
    ys = [int(round(step * (HUD_FIRST_BASELINE + i))) for i in range(n)]

    return {
        'font_scale': font_scale,
        'thickness': thickness,
        'step': step,
        'x': x,
        'ys': ys,
        'block_px': block_px,
    }


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
            # 先腐蚀一下：把刚好接触的细胞之间那点细连接蚀断，避免后续被当成一团
            mask = cv.erode(mask, kernel,
                            iterations=getattr(self.main_window, 'pre_erode_times', PRE_ERODE_TIMES))
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
        self.next_cell_id = 1    # 下一个待发编号（第一帧从 1 开始，最左边的细胞记作 1）
        self.total_count = 0  # 总计数（穿过检测线的细胞数）
        self.exit_border = 0  # 轮廓 bbox 的 x0 ≤ 该值 = 已贴到左边界（正在滑出视野）
        self.max_empty_frames = 10  # 连续空帧上限：超过就清空跟踪（编号计数器仍不回退）
        self.empty_frame_count = 0  # 当前连续空帧计数
        self.frame_width = None  # 当前帧宽度（判断"是否在左边界附近"用）
        self.frame_index = 0     # 帧序号（编号找回记录的过期判断用）
        self.pending_reid = {}   # {宿主编号: [暂存的编号记录, ...]} —— 重叠时被吞掉的编号
        self.pending_reid_orphan = []  # 场上没有宿主可挂的暂存记录（按时间过期）
        self.reid_pending_total = 0   # 累计登记过多少次待找回（调试/统计）
        self.reid_restore_total = 0   # 累计成功找回多少次编号
        self.match_max_distance = MATCH_MAX_DISTANCE  # 帧间匹配的最大移动距离阈值
        self.jump_count = 0           # 累计检测到多少次"整帧平移"并做了补偿
        self.last_jump_shift = None   # 最近一次补偿用的全局位移 (dx, dy)
        self.jump_log = []            # 每次补偿的明细 [{frame, shift, matched_after}, ...]

    @property
    def max_label(self):
        """
        出现过的最大编号 = 这一段视频里曾经出现过的细胞总数。

        编号只增不减、从不复用：细胞从左边滑出视野只是不再跟踪（编号不回收），
        所以视频结束时它就是"曾出现过的细胞总数"。
        """
        return self.next_cell_id - 1
        
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
        mock_window.pre_erode_times = PRE_ERODE_TIMES   # HSV 掩膜先腐蚀的次数（蚀断细胞间的细连接）
        
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
            # 先腐蚀一下：把刚好接触的细胞之间那点细连接蚀断，避免后续被当成一团
            mask = cv.erode(mask, kernel, iterations=self.mock_main_window.pre_erode_times)
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

    def _greedy_match(self, prev_pts, curr_pts, max_distance):
        """
        贪心最近邻匹配：每个前一帧质心找最近的、还没被占用的当前帧质心，距离须小于阈值

        :param prev_pts: 前一帧质心列表 [(x, y), ...]
        :param curr_pts: 当前帧质心列表 [(x, y), ...]
        :param max_distance: 最大移动距离阈值（像素）
        :return: (匹配对 [(prev_idx, curr_idx), ...], 已被占用的当前帧索引集合)
        """
        matched_pairs = []
        used_curr = set()

        for prev_idx, (px, py) in enumerate(prev_pts):
            best_idx = -1
            best_distance = float('inf')

            # 寻找最近的、还没被占用的当前帧轮廓
            for curr_idx, (cx, cy) in enumerate(curr_pts):
                if curr_idx in used_curr:
                    continue
                distance = float(np.hypot(px - cx, py - cy))
                if distance < best_distance:
                    best_distance = distance
                    best_idx = curr_idx

            # 距离不能太远，否则不算匹配
            if best_idx != -1 and best_distance < max_distance:
                matched_pairs.append((prev_idx, best_idx))
                used_curr.add(best_idx)

        return matched_pairs, used_curr

    def estimate_global_shift(self, prev_pts, curr_pts, matched_pairs, used_curr):
        """
        估计帧间的"整帧平移"量（镜头抖动 / 视频跳变时，所有细胞同向位移一大截）

        做法：对没匹配上的细胞，取"它到最近空闲轮廓的位移"的 x、y 中位数（中位数抗离群）。
        位移没超过匹配阈值时返回 None —— 说明只是正常移动，不需要补偿。

        :return: (dx, dy)；不需要补偿时返回 None
        """
        matched_prev = {prev_idx for prev_idx, _ in matched_pairs}
        free_curr = [pt for i, pt in enumerate(curr_pts) if i not in used_curr]
        pending = [pt for i, pt in enumerate(prev_pts) if i not in matched_prev]
        if not free_curr or not pending:
            return None

        # 一对一贪心配对（这里不设距离门限）：多个细胞"各自取最近"会抢同一个轮廓、
        # 把位移估计带偏，必须先一对一配上再统计
        pairs, _ = self._greedy_match(pending, free_curr, float('inf'))
        dxs = [free_curr[j][0] - pending[i][0] for i, j in pairs]
        dys = [free_curr[j][1] - pending[i][1] for i, j in pairs]

        if not dxs:
            return None

        # 至少要有 2 个样本、且其中 ≥2 个位移彼此一致，才认定是"整帧平移"
        # （只有 1 个样本时很容易是"某细胞消失 + 别处冒出新细胞"的乱配对，不能当平移）
        if len(dxs) < 2:
            return None
        dx = float(np.median(dxs))
        dy = float(np.median(dys))
        agree = sum(1 for i in range(len(dxs))
                    if float(np.hypot(dxs[i] - dx, dys[i] - dy)) <= self.match_max_distance)
        if agree < 2:
            return None
        if float(np.hypot(dx, dy)) < self.match_max_distance:
            return None                      # 位移在阈值内，正常匹配就够用
        return dx, dy

    def match_contours(self, prev_contours_with_data, curr_contours):
        """
        匹配前后帧中的轮廓

        整帧平移（镜头抖动 / 视频跳变，所有细胞同向位移一大截）时，普通最近邻匹配会
        集体超出阈值、导致一片编号被当成新细胞重发号；此时先估计全局位移，把上一帧的
        位置平移后再匹配一次，只有"补偿后匹配上的更多"才采用补偿结果。

        :param prev_contours_with_data: 前一帧的轮廓和数据 [(contour, data), ...]
        :param curr_contours: 当前帧的轮廓
        :return: 匹配对列表 [(prev_idx, curr_idx), ...] 和未匹配的轮廓索引
        """
        if not prev_contours_with_data or not curr_contours:
            return [], list(range(len(curr_contours)))

        prev_pts = [self.get_contour_centroid(contour) for contour, _ in prev_contours_with_data]
        curr_pts = [self.get_contour_centroid(contour) for contour in curr_contours]

        # 先按常规（不平移）匹配
        matched_pairs, used_curr = self._greedy_match(prev_pts, curr_pts, self.match_max_distance)

        # 再按"整帧平移补偿后"匹配，谁匹配上的多就用谁
        shift = self.estimate_global_shift(prev_pts, curr_pts, matched_pairs, used_curr)
        if shift is not None:
            dx, dy = shift
            shifted_pts = [(x + dx, y + dy) for x, y in prev_pts]
            pairs_shifted, used_shifted = self._greedy_match(shifted_pts, curr_pts,
                                                             self.match_max_distance)
            if len(pairs_shifted) > len(matched_pairs):
                matched_pairs, used_curr = pairs_shifted, used_shifted
                self.jump_count += 1
                self.last_jump_shift = (dx, dy)
                self.jump_log.append({
                    'frame': self.frame_index,
                    'shift': (dx, dy),
                    'matched_before': len(prev_pts) - len(pairs_shifted),
                    'matched_after': len(pairs_shifted),
                })
                print(f"检测到整帧平移 ({dx:.0f}, {dy:.0f})px，按补偿后的位置匹配，避免编号集体重发")

        # 未匹配的当前帧轮廓
        unmatched_curr = [i for i in range(len(curr_contours)) if i not in used_curr]

        return matched_pairs, unmatched_curr

    def is_out_of_view(self, contour):
        """
        判断细胞是否正从左边滑出视野（轮廓已经贴到左边界）

        检测线计数是"从右往左"穿过，所以左边界就是出口；贴到右边界的是刚进来的
        新细胞，绝不能当滑出处理（否则每帧都会重新发号）。

        :param contour: 轮廓
        :return: True = 已滑出，不再跟踪
        """
        x, _, _, _ = cv.boundingRect(contour)
        return x <= self.exit_border

    def sort_by_centroid_x(self, contours):
        """
        按质心 x 坐标从左到右排序

        :param contours: 轮廓列表
        :return: (排序后的轮廓列表, 对应的质心列表)
        """
        centroids = [self.get_contour_centroid(contour) for contour in contours]
        # 稳定排序：x 相同时保持原顺序
        order = sorted(range(len(contours)), key=lambda i: (centroids[i][0], i))
        return [contours[i] for i in order], [centroids[i] for i in order]

    # ------------------------------------------------------------------
    # 编号找回：两个细胞轮廓合并（后面的快细胞追上前面的慢细胞）时，
    # 被吞掉的那个编号会突然消失；等它们再分离时，把原编号还给分离出来的轮廓。
    # ------------------------------------------------------------------
    def is_near_left_exit(self, contour):
        """
        细胞消失前的中心是否在左边界附近（= 正常流出可视区域，按常规处理，不参与找回）

        :param contour: 消失前最后一帧的轮廓
        :return: True = 正常离开
        """
        if self.is_out_of_view(contour):
            return True
        if self.frame_width:
            cx, _ = self.get_contour_centroid(contour)
            return cx < REID_NEAR_LEFT_RATIO * self.frame_width
        return False

    def is_entering_frame(self, contour):
        """
        轮廓是否贴着右边界（= 刚从右边进来的新细胞）

        【关键判据】只有右侧会流出新细胞，所以"从未出现过的大编号"只可能发给
        贴右边界的轮廓；画面中部冒出来的新轮廓一定是"重叠后又分离"的老细胞。

        :param contour: 轮廓
        :return: True = 贴右边界
        """
        if not self.frame_width:
            return False
        x, _, w, _ = cv.boundingRect(contour)
        return x + w >= self.frame_width * (1.0 - REID_RIGHT_RATIO)

    def are_adjacent(self, contour_a, contour_b):
        """
        两个轮廓是否"贴在一起"（判据：中心距 ≤ REID_ADJACENT_FACTOR × 两者平均尺寸）

        :return: True = 相邻（刚合并/刚分离的形态）
        """
        ca = self.get_contour_centroid(contour_a)
        cb = self.get_contour_centroid(contour_b)
        dist = float(np.hypot(ca[0] - cb[0], ca[1] - cb[1]))
        _, _, wa, ha = cv.boundingRect(contour_a)
        _, _, wb, hb = cv.boundingRect(contour_b)
        size = (max(wa, ha) + max(wb, hb)) / 2.0
        return size > 0 and dist <= REID_ADJACENT_FACTOR * size

    def nearest_left_label(self, contour, tracked_cells):
        """
        找"消失位置左侧、水平方向最近"的细胞编号 —— 大概率就是把它吞掉的合并宿主

        :param contour: 消失前最后一帧的轮廓
        :param tracked_cells: 当前帧跟踪到的细胞
        :return: 宿主编号；左边没有细胞时返回 None
        """
        lx, _ = self.get_contour_centroid(contour)
        best_id, best_dx = None, None
        for cell_id, data in tracked_cells.items():
            cx, _ = self.get_contour_centroid(data['contour'])
            if cx >= lx:                     # 只看左侧
                continue
            dx = lx - cx
            if best_dx is None or dx < best_dx:
                best_id, best_dx = cell_id, dx
        return best_id

    def nearest_host_label(self, lost_contour, tracked_cells):
        """
        找"把消失细胞吞掉"的那个宿主编号

        优先取轮廓真正贴在一起（重叠/合并）的细胞；一个都贴不上时，退回"左侧水平最近"，
        因为在这个流向里，把后车吞掉的通常就是它前面（左侧）那个细胞。

        :param lost_contour: 消失前最后一帧的轮廓
        :param tracked_cells: 当前帧跟踪到的细胞
        :return: 宿主编号；找不到时返回 None
        """
        lx, ly = self.get_contour_centroid(lost_contour)
        best_id, best_dist = None, None
        for cell_id, data in tracked_cells.items():
            if not self.are_adjacent(lost_contour, data['contour']):
                continue                              # 优先：轮廓贴在一起的（真重叠对象）
            cx, cy = self.get_contour_centroid(data['contour'])
            dist = float(np.hypot(cx - lx, cy - ly))
            if best_dist is None or dist < best_dist:
                best_id, best_dist = cell_id, dist
        if best_id is not None:
            return best_id
        return self.nearest_left_label(lost_contour, tracked_cells)

    def _is_label_pending(self, label):
        """
        该编号是否已经暂存（登记会在帧内调用两次，靠它避免重复记录）

        :param label: 编号
        :return: True = 已暂存
        """
        for records in self.pending_reid.values():
            if any(r['label'] == label for r in records):
                return True
        return any(r['label'] == label for r in self.pending_reid_orphan)

    def register_missing_labels(self, updated_tracked_cells):
        """
        把本帧"突然消失"的编号暂存起来，挂在宿主细胞名下

        正常情况下细胞从左侧滑出可视区域 → 直接删除，不暂存；
        中心不在左边界附近就说明是和其他轮廓重叠了 → 暂存编号，等它与宿主分离后归还。

        :param updated_tracked_cells: 本帧更新后的跟踪结果
        """
        for lost_id, lost_data in self.tracked_cells.items():
            if lost_id in updated_tracked_cells:
                continue                                     # 没消失
            if self._is_label_pending(lost_id):
                continue                                     # 本帧已经登记过了
            if self.is_near_left_exit(lost_data['contour']):
                continue                                     # 正常流出可视区域，直接删
            record = {
                'label': lost_id,
                'lost_pos': self.get_contour_centroid(lost_data['contour']),
                'has_crossed': lost_data.get('has_crossed', False),
                'frame': self.frame_index,
            }
            host_id = self.nearest_host_label(lost_data['contour'], updated_tracked_cells)
            self.reid_pending_total += 1
            if host_id is None:
                # 场上没有别的细胞可当宿主（比如它自己就是最左边那个）：照样暂存编号。
                # 因为新编号只可能从右边界发放，它在中部再出现时同样应该归还这个编号。
                self.pending_reid_orphan.append(record)
                print(f"编号 {lost_id} 突然消失（场上没有宿主可挂），暂存编号等待归还")
            else:
                self.pending_reid.setdefault(host_id, []).append(record)
                print(f"编号 {lost_id} 突然消失（疑似与 {host_id} 重叠），暂存编号等待分离后归还")

    def take_restorable_label(self, contour):
        """
        取一个"待归还"的编号：按新轮廓离各消亡位置的距离取最近的

        :param contour: 本帧新出现的轮廓（已确认不在右边界附近）
        :return: 待找回记录 dict（含 'label'）；没有可归还的就返回 None
        """
        if self.is_entering_frame(contour):
            return None
        cx, cy = self.get_contour_centroid(contour)
        best = None                                          # (距离, 宿主编号或 None, 记录下标)
        for host_id, records in self.pending_reid.items():
            for idx, record in enumerate(records):
                dist = float(np.hypot(cx - record['lost_pos'][0], cy - record['lost_pos'][1]))
                if best is None or dist < best[0]:
                    best = (dist, host_id, idx)
        for idx, record in enumerate(self.pending_reid_orphan):   # 没有宿主的暂存记录同样能归还
            dist = float(np.hypot(cx - record['lost_pos'][0], cy - record['lost_pos'][1]))
            if best is None or dist < best[0]:
                best = (dist, None, idx)
        if best is None:
            return None
        dist, host_id, idx = best
        if self.frame_width and dist > REID_MAX_LOST_DIST_RATIO * self.frame_width:
            return None                                      # 离消亡位置太远，不敢认
        if host_id is None:
            record = self.pending_reid_orphan.pop(idx)
        else:
            record = self.pending_reid[host_id].pop(idx)
            if not self.pending_reid[host_id]:
                del self.pending_reid[host_id]
        record['host'] = host_id
        record['dist'] = dist
        return record

    def expire_pending_reid(self, updated_tracked_cells):
        """
        宿主已经不在场上、或者等太久的暂存记录，直接作废

        :param updated_tracked_cells: 本帧更新后的跟踪结果
        """
        for host_id in list(self.pending_reid):
            if host_id not in updated_tracked_cells:
                del self.pending_reid[host_id]
                continue
            records = [r for r in self.pending_reid[host_id]
                       if self.frame_index - r['frame'] <= REID_MAX_FRAMES]
            if records:
                self.pending_reid[host_id] = records
            else:
                del self.pending_reid[host_id]
        # 没有宿主的暂存记录只按时间过期（它们没有宿主可判断是否离场）
        self.pending_reid_orphan = [r for r in self.pending_reid_orphan
                                    if self.frame_index - r['frame'] <= REID_MAX_FRAMES]

    def update_cell_tracking(self, curr_contours, frame_width=None):
        """
        更新细胞跟踪状态
        
        :param curr_contours: 当前帧的轮廓列表
        :param frame_width: 当前帧宽度（用于判断"是否在左边界附近"，可选）
        :return: 更新后的跟踪细胞字典
        """
        if frame_width:
            self.frame_width = frame_width
        self.frame_index += 1
        
        if not curr_contours:
            # 单帧漏检（阈值抖动/细胞短暂模糊）不该把场上细胞的编号清零重发，
            # 否则同一批细胞会被反复当成"新细胞"，最大编号（曾出现过的总数）虚高。
            # 所以先保守保留跟踪；只有连续空帧超过上限才清空（编号计数器不回退）。
            self.empty_frame_count += 1
            if self.empty_frame_count > self.max_empty_frames:
                self.tracked_cells = {}
            else:
                # 标记"本帧没检出"：编号保留，但画面上不重复描上一次的轮廓
                for cell_data in self.tracked_cells.values():
                    cell_data['stale'] = True
            return self.tracked_cells
        
        self.empty_frame_count = 0
        
        # 先把已经从左边滑出视野的细胞从跟踪里剔除：编号不复用、计数器也不回退，只是不再跟踪。
        # 必须提前剔除，否则它会去匹配后面那个细胞、把编号"顶"错位，或者被当成新细胞重复发号。
        if self.tracked_cells:
            self.tracked_cells = {cell_id: data for cell_id, data in self.tracked_cells.items()
                                  if not self.is_out_of_view(data['contour'])}
        
        # 获取前一帧的轮廓和数据
        prev_contours_with_data = [(data['contour'], data) for data in self.tracked_cells.values()]
        prev_ids = list(self.tracked_cells.keys())
        
        if not prev_contours_with_data:
            # 第一帧（或场上细胞全部消失后重新开始）：按质心从左到右编号 1, 2, 3 ...
            # 编号沿用 self.next_cell_id（只增不减），所以重新开始也不会跳回 1
            self.pending_reid = {}          # 场上重新开始，之前的暂存记录作废
            self.pending_reid_orphan = []
            new_tracked_cells = {}
            ordered_contours, ordered_centroids = self.sort_by_centroid_x(curr_contours)
            for contour, centroid in zip(ordered_contours, ordered_centroids):
                new_tracked_cells[self.next_cell_id] = {
                    'contour': contour,
                    'centroid_history': [centroid],  # 记录质心历史
                    'has_crossed': False,  # 是否已穿过检测线
                    'stale': False  # 本帧是否没检出（保留编号但不重描轮廓）
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
                cell_data['stale'] = False
                # 更新质心历史（保留最近几个位置）
                cell_data['centroid_history'].append(centroid)
                if len(cell_data['centroid_history']) > 10:  # 只保留最近10个位置
                    cell_data['centroid_history'] = cell_data['centroid_history'][-10:]
                updated_tracked_cells[prev_id] = cell_data
        
        # 先登记一次（此时宿主只可能是本帧已匹配上的细胞）：这样"本帧刚因位移过大而断开
        # 的轮廓"能立刻在同一帧把自己的编号认领回去，而不是等下一帧被发个新号
        self.register_missing_labels(updated_tracked_cells)
        
        # 新出现的细胞（未匹配上的轮廓）：编号继续往后发（当前最大编号 + 1），
        # 同一帧内多个新细胞也按从左到右的顺序依次编号；
        # 从左边滑出视野的细胞不会走到这里（它已经没有轮廓了），编号不复用。
        # 但刚滑出的那一两帧，它还有半截轮廓贴在左边界上且匹配不上，这种轮廓要丢掉、
        # 不能当新细胞发号，否则每滑出一个细胞总数就虚高一个。
        unmatched_curr = [i for i in unmatched_curr if not self.is_out_of_view(curr_contours[i])]
        if unmatched_curr:
            new_contours = [curr_contours[i] for i in unmatched_curr]
            ordered_contours, ordered_centroids = self.sort_by_centroid_x(new_contours)
            for contour, centroid in zip(ordered_contours, ordered_centroids):
                # 【关键】只有贴着右边界的轮廓才是"新流进来的细胞"，才允许发从未用过的新编号；
                # 画面中部/左侧冒出来的新轮廓一定是"重叠后又分离"的老细胞，
                # 必须归还它原来那个编号，绝不能发新号
                if not self.is_entering_frame(contour):
                    record = self.take_restorable_label(contour)
                    if record is not None and record['label'] not in updated_tracked_cells:
                        label = record['label']
                        updated_tracked_cells[label] = {
                            'contour': contour,
                            # 从分离这一帧重新起算，避免位置跳变被误判为"穿过检测线"
                            'centroid_history': [centroid],
                            'has_crossed': record['has_crossed'],  # 找回的是同一个细胞，继承状态
                            'stale': False
                        }
                        self.reid_restore_total += 1
                        host_txt = '（原暂存记录无宿主）' if record['host'] is None \
                            else f"与宿主 {record['host']} 的轮廓分离"
                        print(f"编号 {label} {host_txt}，找回原编号"
                              f"（x={centroid[0]:.0f}，离消亡位置 {record['dist']:.0f}px，不占新号）")
                        continue
                    print(f"提示：画面中部 x={centroid[0]:.0f} 出现新轮廓，但暂无待归还的编号，"
                          f"按新号处理")
                updated_tracked_cells[self.next_cell_id] = {
                    'contour': contour,
                    'centroid_history': [centroid],
                    'has_crossed': False,
                    'stale': False
                }
                self.next_cell_id += 1
        
        # 发号后再登记一次：这次宿主可以是本帧刚发号的新细胞（否则找不到宿主）；
        # 同一编号不会重复登记（_is_label_pending 拦掉）。最后清理过期记录。
        self.register_missing_labels(updated_tracked_cells)
        self.expire_pending_reid(updated_tracked_cells)
        
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
            # 本帧没检出的细胞：编号保留（不清零重发），但画面上不重复描上一次的轮廓
            if cell_data.get('stale'):
                continue

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

    def hud_lines(self, frame_count, total_frames):
        """
        左侧要显示的几行说明文字（增删行数后字号会自动重算，不用改别的）

        :return: (文字列表, 颜色列表)
        """
        lines = [
            f"Frame: {frame_count}/{total_frames}",
            f"cells passed: {self.total_count}",
            f"cells in view: {len(self.tracked_cells)}",
            f"cells seen: {self.max_label}",
            f"Press 'space' to pause...",
        ]
        colors = [(255, 255, 255), (0, 255, 0), (255, 255, 0), (0, 165, 255), (255, 255, 0)]
        return lines, colors

    def draw_hud(self, frame_display, frame_count, total_frames):
        """
        画左侧说明文字：字号、字粗、行距全部按整张图的尺寸自适应
        （整块高度约为图高的 1/4，见 hud_text_layout）

        :param frame_display: 用于显示的帧（就地绘制）
        :param frame_count: 当前帧号
        :param total_frames: 总帧数
        :return: 本次排版结果 dict
        """
        lines, colors = self.hud_lines(frame_count, total_frames)
        layout = hud_text_layout(frame_display.shape[1], frame_display.shape[0], lines)

        for i, (text, y) in enumerate(zip(lines, layout['ys'])):
            cv.putText(frame_display, text, (layout['x'], y), HUD_FONT,
                       layout['font_scale'], colors[i % len(colors)],
                       layout['thickness'])

        self.hud_layout = layout          # 留一份，方便调试/外部查看当前字号
        return layout

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
            updated_tracked_cells = self.update_cell_tracking(curr_contours, frame_width=width)
            
            # 检查细胞是否穿过检测线
            self.tracked_cells = self.check_crossing_detection_line(updated_tracked_cells, frame_display)
            
            # 显示当前帧信息（左侧几行说明文字，字号/字粗/行距随整图尺寸自适应）
            self.draw_hud(frame_display, frame_count, total_frames)
            
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
        print(f"最终细胞计数（穿过检测线）: {self.total_count}")
        print(f"曾出现过的细胞总数（场上最大编号）: {self.max_label}")
        
        return self.total_count

def main():
    """
    主函数
    """
    # 创建细胞计数器
    counter = VideoCellCounter()
    
    # 使用指定的测试视频
    video_path = os.path.join("refer", "all_count", "mixed.mp4")
    
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
        print(f"整个视频中曾出现过的细胞总数（最大编号）: {counter.max_label}")
        print("="*50)
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main()