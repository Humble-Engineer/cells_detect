import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.animation as animation

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