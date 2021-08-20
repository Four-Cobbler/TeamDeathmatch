# -*- coding: utf-8 -*-
# @Time: 2021-08-18 17:04
# @Author: little kimber
# @File: MAIN.py
import sys
from PyQt5.QtWidgets import (QApplication
                             , QMainWindow
                             , QWidget
                             , QMessageBox, QFileDialog
                             , QDesktopWidget
                             )
from all_ui import divide as divide_ui
from all_ui import welcome as welcome_ui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import time


class WorkThread(QThread):
    START = pyqtSignal()
    END = pyqtSignal()
    def run(self):
        self.START.emit()
        start_time = time.time()
        time.sleep(5)
        end_time = time.time()
        self.work_time = end_time - start_time
        self.END.emit()


class Welcome(QWidget, welcome_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setIcon()
        self.center()
        self.pushButton_2.clicked.connect(self.introduction)

    def introduction(self):
        "这是软件介绍的函数"

        QMessageBox.about(self, "功能介绍", """
        Division是一款图片分割软件
        它可以用来把图片的主题部分提取出来""")

    def center(self):
        "这是使欢迎窗口居中的函数"
        screen = QDesktopWidget().screenGeometry()  # 屏幕坐标系
        size = self.geometry()  # 窗口坐标系
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft, newTop)

    def setIcon(self):
        "这是为界面设置图标的函数"
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.setWindowIcon(icon)


class Divide(QMainWindow, divide_ui.Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setIcon()
        self.pushButton.clicked.connect(self.reSet)
        self.pushButton_3.setDisabled(True)
        self.actionsave.setDisabled(True)
        self.actionsave.triggered.connect(self.save_result)
        self.actionopen_2.triggered.connect(self.getImage)
        self.workThread = WorkThread()
        self.workThread.START.connect(self.start)
        self.workThread.END.connect(self.end)
        self.pushButton_3.clicked.connect(self.work)
        self.pushButton_3.setToolTip("点击按钮开始分割(模拟测试)")
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_2.setToolTip("点击按钮关闭程序")
        self.pushButton_5.clicked.connect(self.reSet)

    def getImage(self):
        "这是获取图片的函数"
        self.pushButton_3.setDisabled(False)  # 只有获取图片后才能开始分割
        self.image_path, self.img_type = QFileDialog.getOpenFileName(None, "打开文件", ".", "")
        self.jpg = QPixmap(self.image_path).scaled(self.label_image.width(), self.label_image.height())
        self.label_image.setPixmap(self.jpg)

    def work(self):
        self.workThread.start()

    def start(self):
        "这是提示图片分割开始的函数"
        self.label_2.setText("图片分割已经开始,请稍等片刻")

    def end(self):
        "这是提示图片分割结束的函数"
        self.actionsave.setDisabled(False)
        self.result = self.label_image.pixmap()
        self.label_result.setPixmap(self.result)
        self.label_2.setText(f"图片分割已经完成,分割时间为{self.workThread.work_time}")

    def setIcon(self):
        "这是为界面设置图标的函数"
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.setWindowIcon(icon)

    def reSet(self):
        "这是用来将图片重置的函数"
        self.label_image.setText("图片导入区")
        self.label_result.setText("结果展示区")
        self.label_2.setText("请重新选择图片")
        self.pushButton_3.setDisabled(True)
        self.actionsave.setDisabled(True)

    def save_result(self):
        "这是用来保存结果的函数"
        filename = QFileDialog.getSaveFileName(None, "保存文件", ".", "Image Files(*.jpg *.png)")
        self.save_picture = self.label_result.pixmap()
        self.save_picture.save(filename[0])
        self.label_2.setText("图片已保存成功,清查收")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = Welcome()
    divide = Divide()
    welcome.pushButton.clicked.connect(divide.show)
    welcome.pushButton.clicked.connect(welcome.close)
    divide.pushButton.clicked.connect(welcome.show)
    divide.pushButton.clicked.connect(divide.close)
    welcome.show()
    sys.exit(app.exec_())
