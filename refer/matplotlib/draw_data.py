import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.animation as animation

# 导入UI文件
from draw_ui import Ui_MainWindow

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        初始化函数，创建一个Matplotlib画布。

        参数:
        - parent: 父容器，用于将画布嵌入到Qt应用程序中。
        - width: 画布宽度（英寸）。
        - height: 画布高度（英寸）。
        - dpi: 每英寸点数，决定了画布的分辨率。
        """
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()  # 实例化UI类
        self.ui.setupUi(self)  # 使用UI类的实例设置主窗口的界面

        # 创建一个Matplotlib画布
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)


        # 在UI文件中指定的位置添加画布（MatLayout为需要取代的布局名称）
        self.ui_layout = self.ui.MatLayout

        if self.ui_layout:
            self.ui_layout.addWidget(self.sc)
        else:
            print("未找到此布局.")



        # 准备一些初始数据
        self.x_data = []  # 初始为空
        self.y_data = []  # 初始为空

        # 基于数据，绘制图形
        self.line, = self.sc.axes.plot([], [], animated=True)
        self.sc.axes.set_title('Rolling Random Data')
        self.sc.axes.set_xlim(0, 9)  # 设置x轴范围
        self.sc.axes.set_xticks(list(range(1, 11)))  # 设置x轴刻度
        self.sc.axes.set_ylim(0, 100)  # 设置y轴范围
        self.sc.axes.axhline(y=50, color='r', linestyle='--')  # 在 y=50 处画一条红色虚线


        # 创建动画
        self.ani = animation.FuncAnimation(
            self.sc.figure,
            self.update_plot,
            init_func=self.init_plot,
            interval=500,
            blit=True,
            cache_frame_data=False
        )

    def init_plot(self):
        """
        初始化绘图函数，设置初始状态。
        """
        self.line.set_data(self.x_data, self.y_data)
        return self.line,

    def update_plot(self, frame):
        """
        更新绘图函数，每秒更新一次。
        """
        # 生成新的数据点
        if self.x_data:  # 如果 self.x_data 不为空
            x_new = self.x_data[-1] + 1  # 取最后一个元素加 1
        else:
            x_new = 0  # 如果 self.x_data 为空，初始化为 0
        y_new = np.random.randint(0, 101)

        # 更新数据列表
        self.x_data.append(x_new)
        self.y_data.append(y_new)

        if len(self.x_data) > 10:
            self.x_data.pop(0)
            self.y_data.pop(0)

            self.sc.axes.set_xlim(self.x_data[0], self.x_data[-1] + 1)  # 设置x轴范围

        # print(self.x_data, self.y_data)

        # 更新图形
        self.line.set_data(self.x_data, self.y_data)

        return self.line,


# 创建并运行应用程序
app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
