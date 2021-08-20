# -*- coding: utf-8 -*-
# @Time: 2021-08-20 15:45
# @Author: little kimber
# @File: second_edition.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import qtawesome

import sys
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt

from custom.stackedWidget import StackedWidget
from custom.treeView import FileSystemTreeView
from custom.listWidgets import FuncListWidget, UsedListWidget
from custom.graphicsView import GraphicsView



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainUI()
    main.show()
    sys.exit(app.exec_())