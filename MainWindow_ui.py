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
        MainWindow.resize(1200, 650)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1200, 650))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
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
        self.result_img = QLabel(self.centralwidget)
        self.result_img.setObjectName(u"result_img")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.result_img.sizePolicy().hasHeightForWidth())
        self.result_img.setSizePolicy(sizePolicy1)
        self.result_img.setMinimumSize(QSize(889, 500))
        self.result_img.setMaximumSize(QSize(889, 500))
        self.result_img.setFrameShape(QFrame.Shape.Panel)

        self.gridLayout.addWidget(self.result_img, 0, 0, 2, 1)

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
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        font1.setItalic(False)
        self.label_3.setFont(font1)
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
        self.S_min_Slider.setValue(0)
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
        self.S_max_Slider.setValue(0)
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
        self.V_min_Slider.setValue(0)
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
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.V_max_Slider.sizePolicy().hasHeightForWidth())
        self.V_max_Slider.setSizePolicy(sizePolicy5)
        self.V_max_Slider.setMaximum(255)
        self.V_max_Slider.setValue(0)
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

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMinimumSize(QSize(0, 0))
        self.label_10.setMaximumSize(QSize(16777215, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_9.addWidget(self.label_11)

        self.Gauss_Slider = QSlider(self.centralwidget)
        self.Gauss_Slider.setObjectName(u"Gauss_Slider")
        sizePolicy3.setHeightForWidth(self.Gauss_Slider.sizePolicy().hasHeightForWidth())
        self.Gauss_Slider.setSizePolicy(sizePolicy3)
        self.Gauss_Slider.setMinimum(0)
        self.Gauss_Slider.setMaximum(4)
        self.Gauss_Slider.setPageStep(1)
        self.Gauss_Slider.setValue(0)
        self.Gauss_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_9.addWidget(self.Gauss_Slider)

        self.Gauss_label = QLabel(self.centralwidget)
        self.Gauss_label.setObjectName(u"Gauss_label")
        sizePolicy4.setHeightForWidth(self.Gauss_label.sizePolicy().hasHeightForWidth())
        self.Gauss_label.setSizePolicy(sizePolicy4)
        self.Gauss_label.setMidLineWidth(4)

        self.horizontalLayout_9.addWidget(self.Gauss_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_10.addWidget(self.label_12)

        self.Struct_Slider = QSlider(self.centralwidget)
        self.Struct_Slider.setObjectName(u"Struct_Slider")
        sizePolicy3.setHeightForWidth(self.Struct_Slider.sizePolicy().hasHeightForWidth())
        self.Struct_Slider.setSizePolicy(sizePolicy3)
        self.Struct_Slider.setMaximum(4)
        self.Struct_Slider.setPageStep(1)
        self.Struct_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_10.addWidget(self.Struct_Slider)

        self.Struct_label = QLabel(self.centralwidget)
        self.Struct_label.setObjectName(u"Struct_label")
        sizePolicy4.setHeightForWidth(self.Struct_label.sizePolicy().hasHeightForWidth())
        self.Struct_label.setSizePolicy(sizePolicy4)
        self.Struct_label.setMidLineWidth(4)

        self.horizontalLayout_10.addWidget(self.Struct_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_11.addWidget(self.label_13)

        self.Erode_Slider = QSlider(self.centralwidget)
        self.Erode_Slider.setObjectName(u"Erode_Slider")
        sizePolicy3.setHeightForWidth(self.Erode_Slider.sizePolicy().hasHeightForWidth())
        self.Erode_Slider.setSizePolicy(sizePolicy3)
        self.Erode_Slider.setMaximum(7)
        self.Erode_Slider.setSingleStep(1)
        self.Erode_Slider.setPageStep(1)
        self.Erode_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_11.addWidget(self.Erode_Slider)

        self.Erode_label = QLabel(self.centralwidget)
        self.Erode_label.setObjectName(u"Erode_label")
        sizePolicy4.setHeightForWidth(self.Erode_label.sizePolicy().hasHeightForWidth())
        self.Erode_label.setSizePolicy(sizePolicy4)
        self.Erode_label.setMidLineWidth(4)

        self.horizontalLayout_11.addWidget(self.Erode_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_12.addWidget(self.label_14)

        self.Dilate_Slider = QSlider(self.centralwidget)
        self.Dilate_Slider.setObjectName(u"Dilate_Slider")
        sizePolicy3.setHeightForWidth(self.Dilate_Slider.sizePolicy().hasHeightForWidth())
        self.Dilate_Slider.setSizePolicy(sizePolicy3)
        self.Dilate_Slider.setMaximum(4)
        self.Dilate_Slider.setPageStep(1)
        self.Dilate_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_12.addWidget(self.Dilate_Slider)

        self.Dilate_label = QLabel(self.centralwidget)
        self.Dilate_label.setObjectName(u"Dilate_label")
        sizePolicy4.setHeightForWidth(self.Dilate_label.sizePolicy().hasHeightForWidth())
        self.Dilate_label.setSizePolicy(sizePolicy4)
        self.Dilate_label.setMidLineWidth(4)

        self.horizontalLayout_12.addWidget(self.Dilate_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")

        self.verticalLayout_2.addLayout(self.horizontalLayout_13)


        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.load_button = QPushButton(self.centralwidget)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.load_button.sizePolicy().hasHeightForWidth())
        self.load_button.setSizePolicy(sizePolicy5)
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(False)
        self.load_button.setFont(font2)

        self.horizontalLayout_7.addWidget(self.load_button)

        self.capture_button = QPushButton(self.centralwidget)
        self.capture_button.setObjectName(u"capture_button")
        self.capture_button.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.capture_button.sizePolicy().hasHeightForWidth())
        self.capture_button.setSizePolicy(sizePolicy5)
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setKerning(True)
        self.capture_button.setFont(font3)

        self.horizontalLayout_7.addWidget(self.capture_button)

        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        sizePolicy5.setHeightForWidth(self.reset_button.sizePolicy().hasHeightForWidth())
        self.reset_button.setSizePolicy(sizePolicy5)
        self.reset_button.setFont(font2)

        self.horizontalLayout_7.addWidget(self.reset_button)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")
        sizePolicy5.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy5)
        self.save_button.setFont(font2)

        self.horizontalLayout_7.addWidget(self.save_button)

        self.draw_button = QPushButton(self.centralwidget)
        self.draw_button.setObjectName(u"draw_button")
        sizePolicy5.setHeightForWidth(self.draw_button.sizePolicy().hasHeightForWidth())
        self.draw_button.setSizePolicy(sizePolicy5)
        font4 = QFont()
        font4.setPointSize(8)
        font4.setBold(True)
        self.draw_button.setFont(font4)

        self.horizontalLayout_7.addWidget(self.draw_button)

        self.fft_button = QPushButton(self.centralwidget)
        self.fft_button.setObjectName(u"fft_button")
        sizePolicy5.setHeightForWidth(self.fft_button.sizePolicy().hasHeightForWidth())
        self.fft_button.setSizePolicy(sizePolicy5)
        self.fft_button.setFont(font4)

        self.horizontalLayout_7.addWidget(self.fft_button)


        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.default_button = QPushButton(self.centralwidget)
        self.default_button.setObjectName(u"default_button")
        sizePolicy5.setHeightForWidth(self.default_button.sizePolicy().hasHeightForWidth())
        self.default_button.setSizePolicy(sizePolicy5)
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setUnderline(False)
        self.default_button.setFont(font5)

        self.horizontalLayout_8.addWidget(self.default_button)

        self.count_button = QPushButton(self.centralwidget)
        self.count_button.setObjectName(u"count_button")
        sizePolicy5.setHeightForWidth(self.count_button.sizePolicy().hasHeightForWidth())
        self.count_button.setSizePolicy(sizePolicy5)
        self.count_button.setFont(font5)

        self.horizontalLayout_8.addWidget(self.count_button)


        self.gridLayout.addLayout(self.horizontalLayout_8, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cell Counter v2.0", None))
        self.result_img.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u503c\u5316\u53c2\u6570", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u8272\u76f8\u4e0b\u9650\uff1a   ", None))
        self.H_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u8272\u76f8\u4e0a\u9650\uff1a   ", None))
        self.H_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u9971\u548c\u5ea6\u4e0a\u9650\uff1a", None))
        self.S_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u9971\u548c\u5ea6\u4e0b\u9650\uff1a", None))
        self.S_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u660e\u5ea6\u4e0a\u9650\uff1a   ", None))
        self.V_min_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u660e\u5ea6\u4e0b\u9650\uff1a   ", None))
        self.V_max_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u5f62\u6001\u5b66\u53c2\u6570", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u65af\u6838\u5c3a\u5bf8\uff1a", None))
        self.Gauss_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u6784\u6838\u5c3a\u5bf8\uff1a", None))
        self.Struct_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u8150\u8680\u7a0b\u5ea6\uff1a   ", None))
        self.Erode_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u81a8\u80c0\u7a0b\u5ea6\uff1a   ", None))
        self.Dilate_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.load_button.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u56fe\u50cf", None))
        self.capture_button.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u56fe\u50cf\uff08\u5f85\u5f00\u53d1\uff09", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d\u539f\u56fe", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u56fe\u50cf", None))
        self.draw_button.setText(QCoreApplication.translate("MainWindow", u"\u7070\u5ea6\u76f4\u65b9\u56fe", None))
        self.fft_button.setText(QCoreApplication.translate("MainWindow", u"\u5085\u91cc\u53f6\u9891\u8c31", None))
        self.default_button.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u53c2\u6570", None))
        self.count_button.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8ba1\u6570", None))
    # retranslateUi

