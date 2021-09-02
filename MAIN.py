# -*- coding: utf-8 -*-
# @Time: 2021-08-31 12:40
# @Author: little kimber
# @File: MAIN.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from My_Widget.FileSystem import MyFileSystem
from My_Widget.GraphicView import My_GraphicsView
from My_Widget.ListWidget import MyListWidget
import u2net_test

class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Division")
        self.setWindowIcon(QIcon("icons/ICON.jpeg"))
        self.resize(700, 600)
        self.filename = None
        self.cur_img = None
        self.src_img = None
        # 下面是工具栏配置区
        self.tool_bar =self.addToolBar("工具栏")
        self.right_rotate_action = QAction(QIcon("icons/right.png"), "向右旋转90度", self)
        self.left_rotate_action = QAction(QIcon("icons/left.png"), "向左旋转90度", self)
        self.refresh_action = QAction(QIcon("icons/refresh.png"), "刷新", self)
        self.right_rotate_action.triggered.connect(self.right_rotate)
        self.left_rotate_action.triggered.connect(self.left_rotate)
        self.refresh_action.triggered.connect(self.refresh)
        self.tool_bar.addActions((self.right_rotate_action, self.left_rotate_action, self.refresh_action))

        # 下面是控件初始化
        self.filesystem = MyFileSystem(self)
        self.graph = My_GraphicsView(self)
        self.listWidget = MyListWidget(self)
        # 下面是区域初始化

        # 目录区域
        self.dock_file = QDockWidget(self)
        self.dock_file.setWidget(self.filesystem)
        self.dock_file.setTitleBarWidget(QLabel("目录"))
        self.dock_file.setFeatures(QDockWidget.NoDockWidgetFeatures)

        # 工作区
        self.dock_func = QDockWidget(self)
        self.dock_func.setWidget(self.listWidget)
        self.dock_func.setTitleBarWidget(QLabel("图片操作"))


        self.setCentralWidget(self.graph)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_file)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_func)

    def right_rotate(self):
        pass

    def left_rotate(self):
        pass

    def refresh(self):
        pass

    def change_img(self, img):
        self.src_img = img          # img 为数组
        self.cur_img = img
        self.graph.change_img(img)

    def update_img(self, img):
        if self.src_img is None:
            return
        self.cur_img = img
        self.graph.update_img(img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styleSheet.qss", encoding='utf-8').read())
    main = Main()
    main.show()
    sys.exit(app.exec_())

