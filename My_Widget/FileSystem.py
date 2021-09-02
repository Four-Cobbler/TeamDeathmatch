# -*- coding: utf-8 -*-
# @Time: 2021-08-31 12:14
# @Author: little kimber
# @File: FileSystem.py
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np

class MyFileSystem(QTreeView, QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainwindow = parent
        self.filesystem = QFileSystemModel()
        self.filesystem.setRootPath(".")
        self.setModel(self.filesystem)
        # 隐藏size,date等列
        self.setColumnWidth(0, 200)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        self.header().hide()
        self.setAnimated(True)
        self.doubleClicked.connect(self.select_img)

    def select_img(self, file_index):
        file_name = self.filesystem.filePath(file_index)
        if file_name.endswith(('.jpg', '.png', 'bmp')):
            src_img = cv2.cvtColor(cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1), cv2.COLOR_BGRA2RGBA)
            self.mainwindow.filename = file_name
            self.mainwindow.change_img(src_img)