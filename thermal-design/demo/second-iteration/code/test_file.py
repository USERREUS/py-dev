#!/usr/bin/python

"""
ZetCode PySide tutorial

This example shows
how to use QtGui.QSplitter widget.

author: Jan Bodnar
website: zetcode.com
"""

import sys
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QStyleFactory, QSplitter, QFrame, QHBoxLayout, QWidget, QMainWindow, \
    QMenuBar, QMenu, QVBoxLayout, QPushButton


class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        hbox = QHBoxLayout(self)
        vbox = QVBoxLayout(self)

        # topleft = QFrame(self)
        # topleft.setFixedSize(200, 20)
        # topleft.setFrameShape(QFrame.StyledPanel)
        #
        # topright = QFrame(self)
        # topright.setFixedSize(200, 20)
        #
        btn = QPushButton("CLOSE")
        # btn.setFixedSize(90, 20)
        btn_2 = QPushButton("OPEN")
        # btn_2.setFixedSize(90, 20)

        # hhbox.setContentsMargins(0, 0, 0, 0)
        #
        # topright.setFrameShape(QFrame.StyledPanel)
        #
        # hbox.addWidget(topleft)
        # hbox.addWidget(topright)
        # vbox.addLayout(hbox)

        lefttop = QFrame(self)
        righttop = QFrame(self)
        righttop.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        lefttop.setFrameShape(QFrame.StyledPanel)
        # lefttop.setStyleSheet("background-color: rgb(255, 255, 255);")
        lefttop.setFrameShadow(QFrame.Raised)
        lefttop.setFixedSize(540, 50)

        righttop.setFrameShape(QFrame.StyledPanel)
        # righttop.setStyleSheet("background-color: rgb(9, 100, 13);")
        righttop.setFrameShadow(QFrame.Raised)
        righttop.setFixedSize(540, 50)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)
        bottom.setFrameShadow(QFrame.Raised)
        # bottom.setStyleSheet("background-color: rgb(166, 5, 13);")

        self.menu_bar = QMenuBar(lefttop)

        self.functions_menu = QMenu("Функции", self)
        self.file_menu = QMenu("Файл", self)
        self.debug_menu = QMenu("Отладка", self)

        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.functions_menu)
        self.menu_bar.addMenu(self.debug_menu)

        self.menu_bar.addAction("Расчет")
        self.menu_bar.addAction("Стоп")
        self.menu_bar.addAction("Очистить")

        for action in self.menu_bar.actions():
            if action.text() == "Стоп":
                action.setEnabled(False)

        self.functions_menu.addAction("Подогреватель")
        self.functions_menu.addAction("Конденсатор")
        self.functions_menu.addAction("Турбина")

        self.file_menu.addAction("Сохранить")  #
        self.file_menu.addAction("Сохранить как...")  #
        self.file_menu.addAction("Загрузить")  #

        self.debug_menu.addAction("Добавить запись в БД")
        self.debug_menu.addAction("Очистить БД")

        self.menu_bar2 = QMenuBar(righttop)

        self.menu_bar2.addAction("X", self.close)
        self.menu_bar2.addAction("[  ]", self.showMaximized)
        self.menu_bar2.addAction("__", self.showMinimized)

        self.menu_bar.setStyleSheet('background-color: #C7EFDECD; padding: 10px; border-bottom: 1px solid black;')
        self.menu_bar2.setStyleSheet('background-color: #C7EFDECD; padding: 10px; border-bottom: 1px solid black;')

        hbox.addWidget(lefttop)
        hbox.addWidget(righttop)

        # hhbox = QHBoxLayout(righttop)
        # hhbox.addWidget(btn)
        # hhbox.addWidget(btn_2)
        # hhbox.setContentsMargins(0, 0, 0, 0)
        # hhbox.setSpacing(0)

        vbox.addLayout(hbox)
        vbox.addWidget(bottom)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # splitter1 = QSplitter(QtCore.Qt.Horizontal)
        # splitter1.addWidget(topleft)
        # splitter1.addWidget(topright)
        #
        # splitter2 = QSplitter(QtCore.Qt.Vertical)
        # splitter2.addWidget(splitter1)
        # splitter2.addWidget(bottom)
        # # splitter2.setEnabled(False)
        # hbox.addWidget(splitter2)

        self.main_widget.setLayout(vbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        # self.menu_bar = QMenuBar(topleft)
        # # hbox.addWidget(self.menu_bar)
        #
        # self.functions_menu = QMenu("Функции", self)
        # self.file_menu = QMenu("Файл", self)
        # self.debug_menu = QMenu("Отладка", self)
        #
        # self.menu_bar.addMenu(self.file_menu)
        # self.menu_bar.addMenu(self.functions_menu)
        # self.menu_bar.addMenu(self.debug_menu)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(1080, 590)
        self.setWindowTitle('TestWindow')
        self.show()


app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec())
