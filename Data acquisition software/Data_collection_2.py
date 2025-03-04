from PySide2.QtCore import QThread, QMutex, Signal
from PySide2.QtWidgets import QApplication
import cv2
import numpy as np
import time
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QMainWindow
from pyorbbecsdk import Pipeline, FrameSet
from pyorbbecsdk import Config
from pyorbbecsdk import OBSensorType, OBFormat
from pyorbbecsdk import OBError
from pyorbbecsdk import VideoStreamProfile
import cv2
import numpy as np
from utils import frame_to_bgr_image
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
from tool import TemporalFilter
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from skeleton_data import draw_landmarks_on_image
import os
import time
import pandas as pd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1101, 738)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 10, 20, 681))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 680, 171, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(170, 10, 20, 681))
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(10, 0, 171, 16))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(190, 10, 20, 591))
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setGeometry(QRect(200, 590, 881, 20))
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)
        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setGeometry(QRect(1010, 10, 151, 591))
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)
        self.line_8 = QFrame(self.centralwidget)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setGeometry(QRect(200, 0, 881, 20))
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 171, 31))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(290, 210, 111, 21))
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(211, 30, 282, 171))
        self.label_8.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(600, 210, 111, 21))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(880, 210, 121, 21))
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(280, 13, 131, 21))
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(580, 10, 161, 21))
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(880, 13, 161, 21))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(220, 660, 151, 28))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(800, 660, 151, 28))
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(500, 30, 282, 171))
        self.label_9.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(790, 30, 282, 171))
        self.label_10.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(790, 230, 282, 171))
        self.label_11.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(211, 230, 282, 171))
        self.label_12.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(500, 230, 282, 171))
        self.label_13.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 160, 171, 31))
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 450, 151, 221))
        self.textBrowser.setStyleSheet(u"background-color: rgb(240, 240, 240);")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(220, 610, 171, 28))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(410, 610, 671, 31))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 210, 151, 231))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)

        self.checkBox_8 = QCheckBox(self.layoutWidget)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.verticalLayout.addWidget(self.checkBox_8)

        self.checkBox_3 = QCheckBox(self.layoutWidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout.addWidget(self.checkBox_3)

        self.checkBox_2 = QCheckBox(self.layoutWidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout.addWidget(self.checkBox_2)

        self.checkBox_4 = QCheckBox(self.layoutWidget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.layoutWidget)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout.addWidget(self.checkBox_5)

        self.checkBox_7 = QCheckBox(self.layoutWidget)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.verticalLayout.addWidget(self.checkBox_7)

        self.checkBox_6 = QCheckBox(self.layoutWidget)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout.addWidget(self.checkBox_6)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(80, 60, 91, 85))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_20 = QLineEdit(self.layoutWidget1)
        self.lineEdit_20.setObjectName(u"lineEdit_20")

        self.verticalLayout_2.addWidget(self.lineEdit_20)

        self.lineEdit_22 = QLineEdit(self.layoutWidget1)
        self.lineEdit_22.setObjectName(u"lineEdit_22")

        self.verticalLayout_2.addWidget(self.lineEdit_22)

        self.lineEdit_21 = QLineEdit(self.layoutWidget1)
        self.lineEdit_21.setObjectName(u"lineEdit_21")

        self.verticalLayout_2.addWidget(self.lineEdit_21)

        self.layoutWidget2 = QWidget(self.centralwidget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 60, 71, 81))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.layoutWidget2)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_3.addWidget(self.label_19)

        self.label_21 = QLabel(self.layoutWidget2)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_3.addWidget(self.label_21)

        self.label_20 = QLabel(self.layoutWidget2)
        self.label_20.setObjectName(u"label_20")

        self.verticalLayout_3.addWidget(self.label_20)

        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(210, 420, 282, 171))
        self.label_17.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(500, 420, 282, 171))
        self.label_18.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_22 = QLabel(self.centralwidget)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(790, 420, 282, 171))
        self.label_22.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        self.label_23 = QLabel(self.centralwidget)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(270, 400, 131, 21))
        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(590, 400, 131, 21))
        self.label_25 = QLabel(self.centralwidget)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(870, 400, 131, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1101, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.checkBox.toggled.connect(self.lineEdit_21.setEnabled)
        self.checkBox.toggled.connect(self.lineEdit_20.setEnabled)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Parameters setting</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">IR Data</span></p></body></html>", None))
        self.label_8.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">OF Data</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Maksed Data</span></p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Front RGB Data</span></p></body></html>", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Skeleton Data</span></p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Depth Data</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start record", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"End record", None))
        self.label_9.setText("")
        self.label_10.setText("")
        self.label_11.setText("")
        self.label_12.setText("")
        self.label_13.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Modal selection</span></p></body></html>", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">A checkmark in front of the checkbox indicates that the relevant modes need to be collected (point cloud modes are not not shown). Extending modality can be further modified if necessary\uff01</span></p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Save Address Settting", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Front RGB Data", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"Up RGB Data", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Depth Data", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Skeleton Data", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"IR Data", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"OF Data", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"Maksed Data", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"PC Data", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"FPS", None))
        self.label_17.setText("")
        self.label_18.setText("")
        self.label_22.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Up RGB Data</span></p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Extending Modality</span></p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:600;\">Extending Modality</span></p></body></html>", None))
    # retranslateUi
class CameraThread(QThread):
    frame_signal = Signal(np.ndarray)  # 用于传递帧数据

    def __init__(self, cam_index, parent=None):
        super(CameraThread, self).__init__(parent)
        self.cam_index = cam_index
        self.cap = None
        self.mutex = QMutex()  # 用于多线程安全的锁机制
        self.running = True

    def run(self):
        self.cap = cv2.VideoCapture(self.cam_index)
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_signal.emit(frame)
            time.sleep(0.05)  # 控制帧率

    def stop(self):
        self.running = False
        self.wait()
        if self.cap:
            self.cap.release()


class MainWindow_RGB(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow_RGB, self).__init__(parent)
        self.setupUi(self)
        self.camera_threads = []
        self.mutex = QMutex()

        # 创建线程并连接信号槽
        self.thread1 = CameraThread(cam_index=3)
        self.thread2 = CameraThread(cam_index=2)

        # 连接信号到不同的展示函数
        self.thread1.frame_signal.connect(self.update_front_rgb)
        self.thread2.frame_signal.connect(self.update_up_rgb)

        # 链接按钮
        self.pushButton.clicked.connect(self.start_threads)
        self.pushButton_2.clicked.connect(self.stop_threads)

    def start_threads(self):
        # 启动线程
        self.thread1.start()
        self.thread2.start()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)

    def stop_threads(self):
        # 停止线程
        self.thread1.stop()
        self.thread2.stop()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)

    def update_front_rgb(self, frame):
        self.mutex.lock()  # 确保多线程安全
        color_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = color_image.shape[0], color_image.shape[1]
        pixmap = QImage(color_image, width, height, 3 * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)

        # 适应窗口播放
        ratio = max(width / self.label_8.width(), height / self.label_8.height())
        pixmap.setDevicePixelRatio(ratio)
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_8.setPixmap(pixmap)
        self.label_8.show()
        self.mutex.unlock()

    def update_up_rgb(self, frame):
        self.mutex.lock()
        color_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = color_image.shape[0], color_image.shape[1]
        pixmap = QImage(color_image, width, height, 3 * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)

        # 适应窗口播放
        ratio = max(width / self.label_17.width(), height / self.label_17.height())
        pixmap.setDevicePixelRatio(ratio)
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_17.setPixmap(pixmap)
        self.label_17.show()
        self.mutex.unlock()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow_RGB()
    main.show()
    sys.exit(app.exec_())
