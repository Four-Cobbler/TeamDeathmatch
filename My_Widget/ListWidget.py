# -*- coding: utf-8 -*-
# @Time: 2021-08-31 17:51
# @Author: little kimber
# @File: ListWidget.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
sys.path.append("..")
import u2net_test

class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainwindow = parent
        self.setFlow(QListWidget.LeftToRight)  # 设置列表方向
        self.setFixedHeight(64)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭滑动条
        self.item_divide = QListWidgetItem(" 图片前景分割 ")
        self.addItem(self.item_divide)
        self.itemClicked.connect(self.divide)

    def divide(self):
        divided_img = u2net_test.MAIN([self.mainwindow.filename])
        self.mainwindow.update_img(divided_img)