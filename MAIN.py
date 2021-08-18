# -*- coding: utf-8 -*-
# @Time: 2021-08-18 17:04
# @Author: little kimber
# @File: MAIN.py
import sys
from PyQt5.QtWidgets import (QApplication
                             , QMainWindow
                             , QWidget
                             , QMessageBox, QFileDialog
                             )
from all_ui import divide as divide_ui
from all_ui import welcome as welcome_ui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import time


class WorkThread(QThread):
    END = pyqtSignal()
    def run(self):
        time.sleep(5)
        self.END.emit()


class Welcome(QWidget, welcome_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.setWindowIcon(icon)
        self.pushButton_2.clicked.connect(self.introduction)

    def introduction(self):
        "这是软件介绍的函数"

        QMessageBox.about(self, "功能介绍", """
        Division是一款图片分割软件
        它可以用来把图片的主题部分提取出来""")


class Divide(QMainWindow, divide_ui.Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.setWindowIcon(icon)
        self.actionopen_2.triggered.connect(self.getImage)

        self.workThread = WorkThread()
        self.workThread.END.connect(self.end)
        self.pushButton_3.clicked.connect(self.work)

    def getImage(self):
        "这是获取图片的函数"

        self.image_path, self.img_type = QFileDialog.getOpenFileName()
        self.jpg = QPixmap(self.image_path).scaled(self.label_image.width(), self.label_image.height())
        self.label_image.setPixmap(self.jpg)

    def work(self):
        self.workThread.start()

    def end(self):
        QMessageBox.about(self, "结束", "图片分割完成")


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
