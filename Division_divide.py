# -*- coding: utf-8 -*-
# @Time: 2021-08-17 15:58
# @Author: little kimber
# @File: Division_divide.py
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import sys

class Divide:
    def __init__(self):
        self.ui = uic.loadUi(r".\all_ui\divide.ui")
        icon = QIcon()
        icon.addPixmap(QPixmap(r".\all_ui\ICON.jpeg"))
        self.ui.setWindowIcon(icon)


if __name__ == '__main__':
    app = QApplication([])
    divide = Divide()
    divide.ui.show()
    app.exec_()