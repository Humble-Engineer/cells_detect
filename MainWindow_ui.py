# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1200, 800))
        MainWindow.setMaximumSize(QSize(1200, 800))
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setIconSize(QSize(48, 48))
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.MatLayout = QVBoxLayout()
        self.MatLayout.setObjectName(u"MatLayout")
        self.MatLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.MatLayout.setContentsMargins(-1, 0, 0, 0)

        self.gridLayout.addLayout(self.MatLayout, 3, 0, 3, 1)

        self.mask_layout = QVBoxLayout()
        self.mask_layout.setSpacing(0)
        self.mask_layout.setObjectName(u"mask_layout")
        self.mask_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(285, 25))
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        font1.setItalic(False)
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mask_layout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(78, 35))

        self.horizontalLayout.addWidget(self.label_4)

        self.H_min_Slider = QSlider(self.centralwidget)
        self.H_min_Slider.setObjectName(u"H_min_Slider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(30)
        sizePolicy2.setHeightForWidth(self.H_min_Slider.sizePolicy().hasHeightForWidth())
        self.H_min_Slider.setSizePolicy(sizePolicy2)
        self.H_min_Slider.setMaximumSize(QSize(185, 9999999))
        self.H_min_Slider.setMaximum(255)
        self.H_min_Slider.setValue(0)
        self.H_min_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.H_min_Slider)

        self.H_min_label = QLabel(self.centralwidget)
        self.H_min_label.setObjectName(u"H_min_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(30)
        sizePolicy3.setHeightForWidth(self.H_min_label.sizePolicy().hasHeightForWidth())
        self.H_min_label.setSizePolicy(sizePolicy3)
        self.H_min_label.setMaximumSize(QSize(24, 35))
        self.H_min_label.setMidLineWidth(4)

        self.horizontalLayout.addWidget(self.H_min_label)


        self.mask_layout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(78, 35))

        self.horizontalLayout_2.addWidget(self.label_5)

        self.H_max_Slider = QSlider(self.centralwidget)
        self.H_max_Slider.setObjectName(u"H_max_Slider")
        sizePolicy2.setHeightForWidth(self.H_max_Slider.sizePolicy().hasHeightForWidth())
        self.H_max_Slider.setSizePolicy(sizePolicy2)
        self.H_max_Slider.setMaximumSize(QSize(185, 9999999))
        self.H_max_Slider.setMaximum(255)
        self.H_max_Slider.setValue(0)
        self.H_max_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.H_max_Slider)

        self.H_max_label = QLabel(self.centralwidget)
        self.H_max_label.setObjectName(u"H_max_label")
        sizePolicy3.setHeightForWidth(self.H_max_label.sizePolicy().hasHeightForWidth())
        self.H_max_label.setSizePolicy(sizePolicy3)
        self.H_max_label.setMaximumSize(QSize(24, 35))
        self.H_max_label.setMidLineWidth(4)

        self.horizontalLayout_2.addWidget(self.H_max_label)


        self.mask_layout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(78, 35))

        self.horizontalLayout_3.addWidget(self.label_6)

        self.S_min_Slider = QSlider(self.centralwidget)
        self.S_min_Slider.setObjectName(u"S_min_Slider")
        sizePolicy2.setHeightForWidth(self.S_min_Slider.sizePolicy().hasHeightForWidth())
        self.S_min_Slider.setSizePolicy(sizePolicy2)
        self.S_min_Slider.setMaximumSize(QSize(185, 9999999))
        self.S_min_Slider.setMaximum(255)
        self.S_min_Slider.setValue(0)
        self.S_min_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.S_min_Slider)

        self.S_min_label = QLabel(self.centralwidget)
        self.S_min_label.setObjectName(u"S_min_label")
        sizePolicy3.setHeightForWidth(self.S_min_label.sizePolicy().hasHeightForWidth())
        self.S_min_label.setSizePolicy(sizePolicy3)
        self.S_min_label.setMaximumSize(QSize(24, 35))
        self.S_min_label.setMidLineWidth(4)

        self.horizontalLayout_3.addWidget(self.S_min_label)


        self.mask_layout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(78, 35))

        self.horizontalLayout_4.addWidget(self.label_7)

        self.S_max_Slider = QSlider(self.centralwidget)
        self.S_max_Slider.setObjectName(u"S_max_Slider")
        sizePolicy2.setHeightForWidth(self.S_max_Slider.sizePolicy().hasHeightForWidth())
        self.S_max_Slider.setSizePolicy(sizePolicy2)
        self.S_max_Slider.setMaximumSize(QSize(185, 9999999))
        self.S_max_Slider.setMaximum(255)
        self.S_max_Slider.setValue(0)
        self.S_max_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.S_max_Slider)

        self.S_max_label = QLabel(self.centralwidget)
        self.S_max_label.setObjectName(u"S_max_label")
        sizePolicy3.setHeightForWidth(self.S_max_label.sizePolicy().hasHeightForWidth())
        self.S_max_label.setSizePolicy(sizePolicy3)
        self.S_max_label.setMaximumSize(QSize(24, 35))
        self.S_max_label.setMidLineWidth(4)

        self.horizontalLayout_4.addWidget(self.S_max_label)


        self.mask_layout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(78, 35))

        self.horizontalLayout_5.addWidget(self.label_8)

        self.V_min_Slider = QSlider(self.centralwidget)
        self.V_min_Slider.setObjectName(u"V_min_Slider")
        sizePolicy2.setHeightForWidth(self.V_min_Slider.sizePolicy().hasHeightForWidth())
        self.V_min_Slider.setSizePolicy(sizePolicy2)
        self.V_min_Slider.setMaximumSize(QSize(185, 9999999))
        self.V_min_Slider.setMaximum(255)
        self.V_min_Slider.setValue(0)
        self.V_min_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.V_min_Slider)

        self.V_min_label = QLabel(self.centralwidget)
        self.V_min_label.setObjectName(u"V_min_label")
        sizePolicy3.setHeightForWidth(self.V_min_label.sizePolicy().hasHeightForWidth())
        self.V_min_label.setSizePolicy(sizePolicy3)
        self.V_min_label.setMaximumSize(QSize(24, 35))
        self.V_min_label.setMidLineWidth(4)

        self.horizontalLayout_5.addWidget(self.V_min_label)


        self.mask_layout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(78, 35))

        self.horizontalLayout_6.addWidget(self.label_9)

        self.V_max_Slider = QSlider(self.centralwidget)
        self.V_max_Slider.setObjectName(u"V_max_Slider")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.V_max_Slider.sizePolicy().hasHeightForWidth())
        self.V_max_Slider.setSizePolicy(sizePolicy4)
        self.V_max_Slider.setMaximumSize(QSize(185, 9999999))
        self.V_max_Slider.setMaximum(255)
        self.V_max_Slider.setValue(0)
        self.V_max_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.V_max_Slider)

        self.V_max_label = QLabel(self.centralwidget)
        self.V_max_label.setObjectName(u"V_max_label")
        sizePolicy3.setHeightForWidth(self.V_max_label.sizePolicy().hasHeightForWidth())
        self.V_max_label.setSizePolicy(sizePolicy3)
        self.V_max_label.setMaximumSize(QSize(24, 35))
        self.V_max_label.setMidLineWidth(4)

        self.horizontalLayout_6.addWidget(self.V_max_label)


        self.mask_layout.addLayout(self.horizontalLayout_6)


        self.gridLayout.addLayout(self.mask_layout, 0, 1, 1, 1)

        self.blur_layout = QVBoxLayout()
        self.blur_layout.setSpacing(0)
        self.blur_layout.setObjectName(u"blur_layout")
        self.blur_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)
        self.label_10.setMinimumSize(QSize(0, 0))
        self.label_10.setMaximumSize(QSize(285, 25))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.blur_layout.addWidget(self.label_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(78, 53))

        self.horizontalLayout_9.addWidget(self.label_11)

        self.Gauss_Slider = QSlider(self.centralwidget)
        self.Gauss_Slider.setObjectName(u"Gauss_Slider")
        sizePolicy2.setHeightForWidth(self.Gauss_Slider.sizePolicy().hasHeightForWidth())
        self.Gauss_Slider.setSizePolicy(sizePolicy2)
        self.Gauss_Slider.setMaximumSize(QSize(185, 9999999))
        self.Gauss_Slider.setMinimum(0)
        self.Gauss_Slider.setMaximum(4)
        self.Gauss_Slider.setPageStep(1)
        self.Gauss_Slider.setValue(0)
        self.Gauss_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_9.addWidget(self.Gauss_Slider)

        self.Gauss_label = QLabel(self.centralwidget)
        self.Gauss_label.setObjectName(u"Gauss_label")
        sizePolicy3.setHeightForWidth(self.Gauss_label.sizePolicy().hasHeightForWidth())
        self.Gauss_label.setSizePolicy(sizePolicy3)
        self.Gauss_label.setMaximumSize(QSize(24, 53))
        self.Gauss_label.setMidLineWidth(4)

        self.horizontalLayout_9.addWidget(self.Gauss_label)


        self.blur_layout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(78, 52))

        self.horizontalLayout_10.addWidget(self.label_12)

        self.Struct_Slider = QSlider(self.centralwidget)
        self.Struct_Slider.setObjectName(u"Struct_Slider")
        sizePolicy2.setHeightForWidth(self.Struct_Slider.sizePolicy().hasHeightForWidth())
        self.Struct_Slider.setSizePolicy(sizePolicy2)
        self.Struct_Slider.setMaximumSize(QSize(185, 9999999))
        self.Struct_Slider.setMaximum(4)
        self.Struct_Slider.setPageStep(1)
        self.Struct_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_10.addWidget(self.Struct_Slider)

        self.Struct_label = QLabel(self.centralwidget)
        self.Struct_label.setObjectName(u"Struct_label")
        sizePolicy3.setHeightForWidth(self.Struct_label.sizePolicy().hasHeightForWidth())
        self.Struct_label.setSizePolicy(sizePolicy3)
        self.Struct_label.setMaximumSize(QSize(24, 53))
        self.Struct_label.setMidLineWidth(4)

        self.horizontalLayout_10.addWidget(self.Struct_label)


        self.blur_layout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(77, 53))

        self.horizontalLayout_11.addWidget(self.label_13)

        self.Erode_Slider = QSlider(self.centralwidget)
        self.Erode_Slider.setObjectName(u"Erode_Slider")
        sizePolicy2.setHeightForWidth(self.Erode_Slider.sizePolicy().hasHeightForWidth())
        self.Erode_Slider.setSizePolicy(sizePolicy2)
        self.Erode_Slider.setMaximumSize(QSize(185, 9999999))
        self.Erode_Slider.setMaximum(7)
        self.Erode_Slider.setSingleStep(1)
        self.Erode_Slider.setPageStep(1)
        self.Erode_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_11.addWidget(self.Erode_Slider)

        self.Erode_label = QLabel(self.centralwidget)
        self.Erode_label.setObjectName(u"Erode_label")
        sizePolicy3.setHeightForWidth(self.Erode_label.sizePolicy().hasHeightForWidth())
        self.Erode_label.setSizePolicy(sizePolicy3)
        self.Erode_label.setMaximumSize(QSize(24, 53))
        self.Erode_label.setMidLineWidth(4)

        self.horizontalLayout_11.addWidget(self.Erode_label)


        self.blur_layout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(77, 53))

        self.horizontalLayout_12.addWidget(self.label_14)

        self.Dilate_Slider = QSlider(self.centralwidget)
        self.Dilate_Slider.setObjectName(u"Dilate_Slider")
        sizePolicy2.setHeightForWidth(self.Dilate_Slider.sizePolicy().hasHeightForWidth())
        self.Dilate_Slider.setSizePolicy(sizePolicy2)
        self.Dilate_Slider.setMaximumSize(QSize(185, 9999999))
        self.Dilate_Slider.setMaximum(4)
        self.Dilate_Slider.setPageStep(1)
        self.Dilate_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_12.addWidget(self.Dilate_Slider)

        self.Dilate_label = QLabel(self.centralwidget)
        self.Dilate_label.setObjectName(u"Dilate_label")
        sizePolicy3.setHeightForWidth(self.Dilate_label.sizePolicy().hasHeightForWidth())
        self.Dilate_label.setSizePolicy(sizePolicy3)
        self.Dilate_label.setMaximumSize(QSize(24, 53))
        self.Dilate_label.setMidLineWidth(4)

        self.horizontalLayout_12.addWidget(self.Dilate_label)


        self.blur_layout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")

        self.blur_layout.addLayout(self.horizontalLayout_13)


        self.gridLayout.addLayout(self.blur_layout, 1, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.fft_button = QPushButton(self.centralwidget)
        self.fft_button.setObjectName(u"fft_button")
        sizePolicy4.setHeightForWidth(self.fft_button.sizePolicy().hasHeightForWidth())
        self.fft_button.setSizePolicy(sizePolicy4)
        self.fft_button.setMinimumSize(QSize(90, 50))
        self.fft_button.setMaximumSize(QSize(9999999, 16777215))
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(True)
        self.fft_button.setFont(font2)

        self.gridLayout_2.addWidget(self.fft_button, 1, 7, 1, 1)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")
        sizePolicy4.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy4)
        self.save_button.setMinimumSize(QSize(90, 50))
        self.save_button.setMaximumSize(QSize(9999999, 16777215))
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        self.save_button.setFont(font3)

        self.gridLayout_2.addWidget(self.save_button, 3, 5, 1, 1)

        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        sizePolicy4.setHeightForWidth(self.reset_button.sizePolicy().hasHeightForWidth())
        self.reset_button.setSizePolicy(sizePolicy4)
        self.reset_button.setMinimumSize(QSize(90, 50))
        self.reset_button.setMaximumSize(QSize(9999999, 16777215))
        self.reset_button.setFont(font3)

        self.gridLayout_2.addWidget(self.reset_button, 1, 5, 1, 1)

        self.capture_button = QPushButton(self.centralwidget)
        self.capture_button.setObjectName(u"capture_button")
        self.capture_button.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.capture_button.sizePolicy().hasHeightForWidth())
        self.capture_button.setSizePolicy(sizePolicy4)
        self.capture_button.setMinimumSize(QSize(90, 50))
        self.capture_button.setMaximumSize(QSize(9999999, 16777215))
        font4 = QFont()
        font4.setPointSize(8)
        font4.setBold(True)
        font4.setItalic(False)
        font4.setUnderline(False)
        font4.setKerning(True)
        self.capture_button.setFont(font4)

        self.gridLayout_2.addWidget(self.capture_button, 3, 3, 1, 1)

        self.load_button = QPushButton(self.centralwidget)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.load_button.sizePolicy().hasHeightForWidth())
        self.load_button.setSizePolicy(sizePolicy4)
        self.load_button.setMinimumSize(QSize(90, 50))
        self.load_button.setMaximumSize(QSize(9999999, 16777215))
        self.load_button.setFont(font3)

        self.gridLayout_2.addWidget(self.load_button, 1, 3, 1, 1)

        self.draw_button = QPushButton(self.centralwidget)
        self.draw_button.setObjectName(u"draw_button")
        sizePolicy4.setHeightForWidth(self.draw_button.sizePolicy().hasHeightForWidth())
        self.draw_button.setSizePolicy(sizePolicy4)
        self.draw_button.setMinimumSize(QSize(90, 50))
        self.draw_button.setMaximumSize(QSize(9999999, 16777215))
        self.draw_button.setFont(font2)

        self.gridLayout_2.addWidget(self.draw_button, 3, 7, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 3, 1, 1, 1)

        self.count_layout = QHBoxLayout()
        self.count_layout.setObjectName(u"count_layout")
        self.count_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.default_button = QPushButton(self.centralwidget)
        self.default_button.setObjectName(u"default_button")
        sizePolicy4.setHeightForWidth(self.default_button.sizePolicy().hasHeightForWidth())
        self.default_button.setSizePolicy(sizePolicy4)
        self.default_button.setMinimumSize(QSize(0, 0))
        self.default_button.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setUnderline(False)
        self.default_button.setFont(font5)

        self.count_layout.addWidget(self.default_button)

        self.count_button = QPushButton(self.centralwidget)
        self.count_button.setObjectName(u"count_button")
        sizePolicy4.setHeightForWidth(self.count_button.sizePolicy().hasHeightForWidth())
        self.count_button.setSizePolicy(sizePolicy4)
        self.count_button.setMinimumSize(QSize(0, 0))
        self.count_button.setMaximumSize(QSize(16777215, 16777215))
        self.count_button.setFont(font5)

        self.count_layout.addWidget(self.count_button)


        self.gridLayout.addLayout(self.count_layout, 5, 1, 1, 1)

        self.result_img = QLabel(self.centralwidget)
        self.result_img.setObjectName(u"result_img")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.result_img.sizePolicy().hasHeightForWidth())
        self.result_img.setSizePolicy(sizePolicy5)
        self.result_img.setMinimumSize(QSize(890, 500))
        self.result_img.setMaximumSize(QSize(16777215, 16777215))
        self.result_img.setFrameShape(QFrame.Shape.Panel)

        self.gridLayout.addWidget(self.result_img, 0, 0, 3, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.count_type_Box = QCheckBox(self.centralwidget)
        self.count_type_Box.setObjectName(u"count_type_Box")
        self.count_type_Box.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.count_type_Box.setTristate(False)

        self.horizontalLayout_7.addWidget(self.count_type_Box)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.write_file_Box = QCheckBox(self.centralwidget)
        self.write_file_Box.setObjectName(u"write_file_Box")

        self.horizontalLayout_7.addWidget(self.write_file_Box)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cell Counter v3.0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Binary args", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"H MIN", None))
        self.H_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"H MAX", None))
        self.H_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"S MIN", None))
        self.S_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"S MAX", None))
        self.S_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"V MIN", None))
        self.V_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"V MAX", None))
        self.V_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Morphological args", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Gaussian", None))
        self.Gauss_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Structural", None))
        self.Struct_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Corrosion", None))
        self.Erode_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Expansion", None))
        self.Dilate_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.fft_button.setText(QCoreApplication.translate("MainWindow", u"fft img", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"save img", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"renew img", None))
        self.capture_button.setText(QCoreApplication.translate("MainWindow", u"capture img", None))
        self.load_button.setText(QCoreApplication.translate("MainWindow", u"load img", None))
        self.draw_button.setText(QCoreApplication.translate("MainWindow", u"hist img", None))
        self.default_button.setText(QCoreApplication.translate("MainWindow", u"default args", None))
        self.count_button.setText(QCoreApplication.translate("MainWindow", u"start count", None))
        self.result_img.setText("")
        self.count_type_Box.setText(QCoreApplication.translate("MainWindow", u"outline only", None))
        self.write_file_Box.setText(QCoreApplication.translate("MainWindow", u"logging data", None))
    # retranslateUi

