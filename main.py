'''
打包发布命令：
pyinstaller -F -w --icon=./libs/cell.ico main.py
-w (–windowed / –noconsole): 对于 GUI 应用程序，隐藏控制台窗口。
--icon=FILE.ico: 指定可执行文件的图标。
'''

import sys
import cv2

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon

from MainWindow_ui import Ui_MainWindow

from modules.basic import Basic
from modules.camera import Camera
from modules.statistics import Statistics
from modules.algorithm import Algorithm
from modules.draw import MplCanvas
from modules.record import DataHandler


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

        self.basic = Basic(self) # 加载、保存、重置图像等功能
        self.camera = Camera(self) # 相机相关函数

        self.statistics = Statistics(self)  # 统计相关函数
        self.algorithm = Algorithm(self)    # 图像处理相关函数

        self.mat = MplCanvas(self)  # 创建一个Matplotlib画布
        
        self.handler = DataHandler(self) # 数据存储功能

        self.slot_bind()  # 调用band方法进行进一步的初始化或设置
        self.argu_init()  # 设置默认参数

        screen = cv2.imread('libs/logo3.png')
        self.basic.display_image(screen)

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

        self.ui.load_button.clicked.connect(self.basic.load_image)
        self.ui.save_button.clicked.connect(self.basic.save_image)
        self.ui.reset_button.clicked.connect(self.basic.reset_image)

        self.ui.draw_button.clicked.connect(self.statistics.darw_hist)
        self.ui.fft_button.clicked.connect(self.statistics.fast_fft)

        self.ui.default_button.clicked.connect(self.argu_init)
        self.ui.count_button.clicked.connect(self.algorithm.count)
        self.ui.capture_button.clicked.connect(self.camera.toggle_thread)

        self.ui.write_file_Box.stateChanged.connect(self.handler.change_record_mode)
        self.ui.count_type_Box.stateChanged.connect(self.algorithm.detect_type)

        self.sliders = [self.ui.H_min_Slider, self.ui.H_max_Slider, self.ui.S_min_Slider,
                        self.ui.S_max_Slider, self.ui.V_min_Slider, self.ui.V_max_Slider,

                        self.ui.Gauss_Slider, self.ui.Struct_Slider, 
                        self.ui.Erode_Slider, self.ui.Dilate_Slider]
        
        for slider in self.sliders:
            slider.sliderReleased.connect(self.argu_update)
            slider.sliderMoved.connect(self.argu_update)
            slider.valueChanged.connect(self.argu_update)

    def argu_init(self):

        self.ui.H_min_Slider.setValue(30)
        self.ui.H_max_Slider.setValue(90)
        self.ui.S_min_Slider.setValue(70)
        self.ui.S_max_Slider.setValue(255)
        self.ui.V_min_Slider.setValue(70)
        self.ui.V_max_Slider.setValue(255)

        self.ui.Gauss_Slider.setValue(1)
        self.ui.Struct_Slider.setValue(1)
        self.ui.Erode_Slider.setValue(0)
        self.ui.Dilate_Slider.setValue(1)

        self.low_percentage = 0.4
        self.growth_factor = 1.75
        self.border_distance = 10

        self.argu_update()
        # print("检测参数已经重置...")

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


if __name__ == "__main__":
    # 创建 QApplication 实例
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('libs/cell.ico'))

    # 创建主窗口并显示
    main_window = MainWindow()
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec())