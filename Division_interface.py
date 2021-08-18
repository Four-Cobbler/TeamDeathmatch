# -*- coding: utf-8 -*-
# @Time: 2021-08-17 14:26
# @Author: little kimber
# @File: Division_interface.py
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication,
                             QMessageBox,
                             QFileDialog,
                             QAction,
                             QLabel,
                             QMenuBar)
from PyQt5.QtGui import QIcon, QPixmap
import time
import sys
from threading import Thread

class Welcome:
    def __init__(self):
        self.ui = uic.loadUi(r".\all_ui\welcome.ui")
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.ui.setWindowIcon(icon)
        self.ui.pushButton_2.clicked.connect(self.introduction)

    def introduction(self):
        "这是软件介绍的函数"

        QMessageBox.about(self.ui, "功能介绍", """
        Division是一款图片分割软件
        它可以用来把图片的主题部分提取出来""")



class Divide:
    def __init__(self):
        self.ui = uic.loadUi(r".\all_ui\divide.ui")
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.ui.setWindowIcon(icon)
        self.ui.pushButton.clicked.connect(self.ui.close)
        self.ui.pushButton_2.clicked.connect(self.ui.close)
        self.ui.actionopen_2.triggered.connect(self.getImage)
        self.ui.pushButton_4.clicked.connect(self.all_thread)
        self.ui.pushButton_3.clicked.connect(self.talk)
    def getImage(self):
        "这是获取图片的函数"

        self.image_path, self.img_type = QFileDialog.getOpenFileName()
        self.jpg = QPixmap(self.image_path).scaled(self.ui.label_image.width(), self.ui.label_image.height())
        self.ui.label_image.setPixmap(self.jpg)

    def all_thread(self):

        thread1 = Thread(target=self.picture_divide)
        thread1.start()




    def picture_divide(self):
        "这是模拟图片分割的函数"
        time.sleep(5)

        QMessageBox.about(self.ui, "结果", "恭喜您，已经分割完成啦")

    def talk(self):
        time.sleep(5)
        QMessageBox.about(self.ui, "talk", "我在说话啦啦啦")




def main():
    app = QApplication(sys.argv)
    welcome = Welcome()
    divide = Divide()
    divide.ui.pushButton.clicked.connect(welcome.ui.show)
    welcome.ui.pushButton.clicked.connect(divide.ui.show)
    welcome.ui.pushButton.clicked.connect(welcome.ui.close)
    welcome.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()