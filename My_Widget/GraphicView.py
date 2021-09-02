# -*- coding: utf-8 -*-
# @Time: 2021-08-31 12:14
# @Author: little kimber
# @File: GraphicView.py
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
from PyQt5.QtGui import *
import numpy as np
from PIL import Image

class My_GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom = 0  # 控制图片放大还是缩小
        self.empty = True  # 判断是否有图片的变量
        self.imgItem = QGraphicsPixmapItem()  # 设置显示pixmap的控件
        self.img = QPixmap()
        self.scene = QGraphicsScene()
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene.addItem(self.imgItem)
        self.setScene(self.scene)

    def contextMenuEvent(self, event):
        if not self.has_photo():
            return
        menu = QMenu()
        save_action = QAction("另存为", self)
        save_action.triggered.connect(self.save)
        menu.exec_(QCursor.pos())

    def has_photo(self):
        "判断view里是否有图片的函数"
        return not self.empty

    def save(self):
        "保存图片的函数"
        file_name = QFileDialog.getSaveFileName(self, "另存为", "./", "Image files(*.jpg *.png *.gif)")[0]
        if file_name:
            self.imgItem.pixmap().save(file_name)

    def fitInView(self, scale=True):
        rect = QRectF(self.imgItem.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self.zoom = 0

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom += 1
        else:
            factor = 0.8
            self.zoom -= 1
        if self.zoom > 0:
            self.scale(factor, factor)
        elif self.zoom < 0:
            self.scale(factor, factor)

    def change_img(self, img):
        self.update_img(img)
        self.fitInView()

    def update_img(self, img):
        self.empty = False
        self.imgItem.setPixmap(self.img_to_pixmap(img))

    def img_to_pixmap(self, img):
        img = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(img)
        return pixmap
