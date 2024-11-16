from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import threading
import time

import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class MplCanvas(FigureCanvas):
    def __init__(self, main_window):
        """
        初始化函数，创建一个Matplotlib画布。
        """
        self.main_window = main_window
        main_window.mat = self
        
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        # 在UI文件中指定的位置添加画布
        self.main_window.ui_layout = self.main_window.ui.MatLayout

        if self.main_window.ui_layout:
            self.main_window.ui_layout.addWidget(self.main_window.mat)
        else:
            print("未找到此布局.")

        # 准备一些初始数据
        self.main_window.x_data = []  # 初始为空
        self.main_window.y_data = []  # 初始为空

        # 基于数据，绘制图形
        self.line, = self.main_window.mat.axes.plot([], [], animated=True)
        self.main_window.mat.axes.set_title('计数结果')
        self.main_window.mat.axes.set_xlim(0, 29)  # 设置x轴范围
        self.main_window.mat.axes.set_xticks(list(range(1, 31)))  # 设置x轴刻度
        self.main_window.mat.axes.tick_params(axis='x', labelsize=6)  # 调整x轴标签字体大小
        self.main_window.mat.axes.set_ylim(0, 500)  # 设置y轴范围
        self.main_window.mat.axes.tick_params(axis='y', labelsize=6)  # 调整y轴标签字体大小
        self.main_window.mat.axes.axhline(y=300, color='r', linestyle='--')  # 在 y=300 处画一条红色虚线


        # 创建动画
        self.ani = animation.FuncAnimation(
            self.main_window.mat.figure,
            self.update_plot,
            init_func=self.init_plot,
            interval=1000,
            blit=True,
            cache_frame_data=False
        )

    def init_plot(self):
        """
        初始化绘图函数，设置初始状态。
        """
        self.line.set_data(self.main_window.x_data, self.main_window.y_data)
        return self.line,

    def update_plot(self, frame):
        """
        更新绘图函数，每秒更新一次。
        """
        # 更新数据列表
        if len(self.main_window.x_data) > 30:
            while len(self.main_window.x_data) > 30:
                self.main_window.x_data.pop(0)
                self.main_window.y_data.pop(0)

            # 更新 x 轴范围和刻度
            self.main_window.mat.axes.set_xlim(self.main_window.x_data[0], self.main_window.x_data[-1] + 1)
            self.main_window.mat.axes.set_xticks(list(range(self.main_window.x_data[0], self.main_window.x_data[-1] + 2)))

        # 清除之前的注释
        texts_to_remove = self.main_window.mat.axes.texts[:]
        for text in texts_to_remove:
            text.remove()

        # 更新图形
        self.line.set_data(self.main_window.x_data, self.main_window.y_data)

        # 添加注释
        for i, (x, y) in enumerate(zip(self.main_window.x_data, self.main_window.y_data)):
            self.main_window.mat.axes.text(x, y + 5, f'{y:.0f}', ha='center', fontsize=8)

        # 添加红色标记点
        self.main_window.mat.axes.scatter(self.main_window.x_data, self.main_window.y_data, color='red', s=15)

        # 强制更新图形
        self.main_window.mat.figure.canvas.draw()

        return self.line,

    def add_data(self, y):
        """
        添加数据到绘图。
        """
        # 生成新的数据点
        if self.main_window.x_data:  # 如果 self.x_data 不为空
            x_new = self.main_window.x_data[-1] + 1  # 取最后一个元素加 1
        else:
            x_new = 0  # 如果 self.x_data 为空，初始化为 0
        y_new = y

        # 更新数据列表
        self.main_window.x_data.append(x_new)
        self.main_window.y_data.append(y_new)

    def start_thread(self):
        self.thread_running = True
        self.worker_thread = threading.Thread(target=self.thread_worker, daemon=True)
        self.worker_thread.start()

    def stop_thread(self):
        self.thread_running = False
        if self.worker_thread is not None:
            self.worker_thread.join()
        self.worker_thread = None

    def thread_worker(self):
        while self.thread_running:
            self.update_plot(self.main_window.mat.figure)
            time.sleep(1)