
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.animation as animation

import time

class MplCanvas(FigureCanvas):
    def __init__(self, main_window):
        """
        初始化函数，创建一个Matplotlib画布。

        参数:
        - parent: 父容器，用于将画布嵌入到Qt应用程序中。
        - width: 画布宽度（英寸）。
        - height: 画布高度（英寸）。
        - dpi: 每英寸点数，决定了画布的分辨率。
        """

        self.main_window = main_window
        main_window.mat = self
        
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    
        # 在UI文件中指定的位置添加画布（MatLayout为需要取代的布局名称）
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
        self.main_window.mat.axes.set_title('Rolling Random Data')
        self.main_window.mat.axes.set_xlim(0, 19)  # 设置x轴范围
        self.main_window.mat.axes.set_xticks(list(range(1, 21)))  # 设置x轴刻度
        # self.main_window.mat.axes.set_xticks([])    # 不显示x轴刻度
        self.main_window.mat.axes.set_ylim(0, 500)  # 设置y轴范围
        self.main_window.mat.axes.axhline(y=300, color='r', linestyle='--')  # 在 y=50 处画一条红色虚线

        # 创建动画
        self.ani = animation.FuncAnimation(
            self.main_window.mat.figure,
            self.update_plot,
            init_func=self.init_plot,
            interval=100,
            blit=True,
            cache_frame_data=False
        )

        # 添加一些数据点
        for i in range(10):
            self.add_data(np.random.randint(0, 501))

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

        if len(self.main_window.x_data) > 20:
            self.main_window.x_data.pop(0)
            self.main_window.y_data.pop(0)

            self.main_window.mat.axes.set_xlim(self.main_window.x_data[0], self.main_window.x_data[-1] + 1)  # 设置x轴范围
            self.main_window.mat.axes.set_xticks(list(range(self.main_window.x_data[0], self.main_window.x_data[-1] + 2)))  # 设置x轴刻度
            self.main_window.mat.figure.canvas.draw()  # 强制更新图形
            
        # print(self.x_data, self.y_data)

        # 更新图形
        self.line.set_data(self.main_window.x_data, self.main_window.y_data)

        return self.line,

    def add_data(self,y):
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
