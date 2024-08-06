# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1200, 600))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.default_button = QPushButton(self.centralwidget)
        self.default_button.setObjectName(u"default_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.default_button.sizePolicy().hasHeightForWidth())
        self.default_button.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        self.default_button.setFont(font1)

        self.horizontalLayout_8.addWidget(self.default_button)

        self.count_button = QPushButton(self.centralwidget)
        self.count_button.setObjectName(u"count_button")
        sizePolicy1.setHeightForWidth(self.count_button.sizePolicy().hasHeightForWidth())
        self.count_button.setSizePolicy(sizePolicy1)
        self.count_button.setFont(font1)

        self.horizontalLayout_8.addWidget(self.count_button)


        self.gridLayout.addLayout(self.horizontalLayout_8, 1, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        font2.setItalic(False)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.H_min_Slider = QSlider(self.centralwidget)
        self.H_min_Slider.setObjectName(u"H_min_Slider")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(30)
        sizePolicy3.setHeightForWidth(self.H_min_Slider.sizePolicy().hasHeightForWidth())
        self.H_min_Slider.setSizePolicy(sizePolicy3)
        self.H_min_Slider.setMaximum(255)
        self.H_min_Slider.setValue(0)
        self.H_min_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.H_min_Slider)

        self.H_min_label = QLabel(self.centralwidget)
        self.H_min_label.setObjectName(u"H_min_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(30)
        sizePolicy4.setHeightForWidth(self.H_min_label.sizePolicy().hasHeightForWidth())
        self.H_min_label.setSizePolicy(sizePolicy4)
        self.H_min_label.setMidLineWidth(4)

        self.horizontalLayout.addWidget(self.H_min_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.H_max_Slider = QSlider(self.centralwidget)
        self.H_max_Slider.setObjectName(u"H_max_Slider")
        sizePolicy3.setHeightForWidth(self.H_max_Slider.sizePolicy().hasHeightForWidth())
        self.H_max_Slider.setSizePolicy(sizePolicy3)
        self.H_max_Slider.setMaximum(255)
        self.H_max_Slider.setValue(0)
        self.H_max_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.H_max_Slider)

        self.H_max_label = QLabel(self.centralwidget)
        self.H_max_label.setObjectName(u"H_max_label")
        sizePolicy4.setHeightForWidth(self.H_max_label.sizePolicy().hasHeightForWidth())
        self.H_max_label.setSizePolicy(sizePolicy4)
        self.H_max_label.setMidLineWidth(4)

        self.horizontalLayout_2.addWidget(self.H_max_label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.S_min_Slider = QSlider(self.centralwidget)
        self.S_min_Slider.setObjectName(u"S_min_Slider")
        sizePolicy3.setHeightForWidth(self.S_min_Slider.sizePolicy().hasHeightForWidth())
        self.S_min_Slider.setSizePolicy(sizePolicy3)
        self.S_min_Slider.setMaximum(255)
        self.S_min_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.S_min_Slider)

        self.S_min_label = QLabel(self.centralwidget)
        self.S_min_label.setObjectName(u"S_min_label")
        sizePolicy4.setHeightForWidth(self.S_min_label.sizePolicy().hasHeightForWidth())
        self.S_min_label.setSizePolicy(sizePolicy4)
        self.S_min_label.setMidLineWidth(4)

        self.horizontalLayout_3.addWidget(self.S_min_label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.S_max_Slider = QSlider(self.centralwidget)
        self.S_max_Slider.setObjectName(u"S_max_Slider")
        sizePolicy3.setHeightForWidth(self.S_max_Slider.sizePolicy().hasHeightForWidth())
        self.S_max_Slider.setSizePolicy(sizePolicy3)
        self.S_max_Slider.setMaximum(255)
        self.S_max_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.S_max_Slider)

        self.S_max_label = QLabel(self.centralwidget)
        self.S_max_label.setObjectName(u"S_max_label")
        sizePolicy4.setHeightForWidth(self.S_max_label.sizePolicy().hasHeightForWidth())
        self.S_max_label.setSizePolicy(sizePolicy4)
        self.S_max_label.setMidLineWidth(4)

        self.horizontalLayout_4.addWidget(self.S_max_label)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.V_min_Slider = QSlider(self.centralwidget)
        self.V_min_Slider.setObjectName(u"V_min_Slider")
        sizePolicy3.setHeightForWidth(self.V_min_Slider.sizePolicy().hasHeightForWidth())
        self.V_min_Slider.setSizePolicy(sizePolicy3)
        self.V_min_Slider.setMaximum(255)
        self.V_min_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.V_min_Slider)

        self.V_min_label = QLabel(self.centralwidget)
        self.V_min_label.setObjectName(u"V_min_label")
        sizePolicy4.setHeightForWidth(self.V_min_label.sizePolicy().hasHeightForWidth())
        self.V_min_label.setSizePolicy(sizePolicy4)
        self.V_min_label.setMidLineWidth(4)

        self.horizontalLayout_5.addWidget(self.V_min_label)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.V_max_Slider = QSlider(self.centralwidget)
        self.V_max_Slider.setObjectName(u"V_max_Slider")
        sizePolicy1.setHeightForWidth(self.V_max_Slider.sizePolicy().hasHeightForWidth())
        self.V_max_Slider.setSizePolicy(sizePolicy1)
        self.V_max_Slider.setMaximum(255)
        self.V_max_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.V_max_Slider)

        self.V_max_label = QLabel(self.centralwidget)
        self.V_max_label.setObjectName(u"V_max_label")
        sizePolicy4.setHeightForWidth(self.V_max_label.sizePolicy().hasHeightForWidth())
        self.V_max_label.setSizePolicy(sizePolicy4)
        self.V_max_label.setMidLineWidth(4)

        self.horizontalLayout_6.addWidget(self.V_max_label)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.load_button = QPushButton(self.centralwidget)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.load_button.sizePolicy().hasHeightForWidth())
        self.load_button.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setUnderline(False)
        self.load_button.setFont(font3)

        self.horizontalLayout_7.addWidget(self.load_button)

        self.capture_button = QPushButton(self.centralwidget)
        self.capture_button.setObjectName(u"capture_button")
        self.capture_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.capture_button.sizePolicy().hasHeightForWidth())
        self.capture_button.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(8)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setUnderline(False)
        font4.setKerning(True)
        self.capture_button.setFont(font4)

        self.horizontalLayout_7.addWidget(self.capture_button)

        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        sizePolicy1.setHeightForWidth(self.reset_button.sizePolicy().hasHeightForWidth())
        self.reset_button.setSizePolicy(sizePolicy1)
        self.reset_button.setFont(font3)

        self.horizontalLayout_7.addWidget(self.reset_button)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")
        sizePolicy1.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy1)
        self.save_button.setFont(font3)

        self.horizontalLayout_7.addWidget(self.save_button)

        self.draw_button = QPushButton(self.centralwidget)
        self.draw_button.setObjectName(u"draw_button")
        sizePolicy1.setHeightForWidth(self.draw_button.sizePolicy().hasHeightForWidth())
        self.draw_button.setSizePolicy(sizePolicy1)
        font5 = QFont()
        font5.setPointSize(8)
        font5.setBold(False)
        self.draw_button.setFont(font5)

        self.horizontalLayout_7.addWidget(self.draw_button)

        self.fft_button = QPushButton(self.centralwidget)
        self.fft_button.setObjectName(u"fft_button")
        sizePolicy1.setHeightForWidth(self.fft_button.sizePolicy().hasHeightForWidth())
        self.fft_button.setSizePolicy(sizePolicy1)
        self.fft_button.setFont(font5)

        self.horizontalLayout_7.addWidget(self.fft_button)


        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.result_img = QLabel(self.centralwidget)
        self.result_img.setObjectName(u"result_img")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.result_img.sizePolicy().hasHeightForWidth())
        self.result_img.setSizePolicy(sizePolicy5)
        self.result_img.setMinimumSize(QSize(889, 500))
        self.result_img.setMaximumSize(QSize(889, 500))
        self.result_img.setFrameShape(QFrame.Shape.Panel)

        self.gridLayout.addWidget(self.result_img, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cell Count", None))
        self.default_button.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u53c2\u6570", None))
        self.count_button.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8ba1\u6570", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u503c\u5316\u53c2\u6570", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"H min", None))
        self.H_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"H max", None))
        self.H_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"S min", None))
        self.S_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"S max", None))
        self.S_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"V min", None))
        self.V_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"V max", None))
        self.V_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.load_button.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u56fe\u50cf", None))
        self.capture_button.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u56fe\u50cf", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d\u539f\u56fe", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u56fe\u50cf", None))
        self.draw_button.setText(QCoreApplication.translate("MainWindow", u"\u7070\u5ea6\u76f4\u65b9\u56fe", None))
        self.fft_button.setText(QCoreApplication.translate("MainWindow", u"\u5085\u91cc\u53f6\u9891\u8c31", None))
        self.result_img.setText("")
    # retranslateUi

