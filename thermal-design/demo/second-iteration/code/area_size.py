#!/usr/bin/python

"""
ZetCode PySide tutorial

This example shows
how to use QtGui.QComboBox widget.

author: Jan Bodnar
website: zetcode.com
"""

import sys
from PySide6 import QtGui, QtCore
from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, \
    QMainWindow, QFrame, QMenuBar, QTextEdit


class OnLoadSetuper(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setFixedSize(300, 200)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("border: 1px solid black; ")

        self.hbox = QHBoxLayout(self)
        self.vbox = QVBoxLayout(self)

        self.lefttop = QFrame(self)
        self.righttop = QFrame(self)
        self.window_icon = QFrame(self)

        self.righttop.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        self.lefttop.setFrameShape(QFrame.StyledPanel)
        self.lefttop.setStyleSheet("border: none;")
        self.lefttop.setFrameShadow(QFrame.Raised)
        self.lefttop.setFixedSize(int(self.width() / 2) - 40, 50)

        self.window_icon.setFrameShape(QFrame.StyledPanel)
        self.window_icon.setStyleSheet("border: none;")
        self.window_icon.setFrameShadow(QFrame.Raised)
        self.window_icon.setFixedSize(40, 50)

        self.righttop.setFrameShape(QFrame.StyledPanel)
        self.righttop.setStyleSheet("border: none;")
        self.righttop.setFrameShadow(QFrame.Raised)
        self.righttop.setFixedSize(int(self.width() / 2), 50)

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setStyleSheet("border: none;")
        self.bottom.setFrameShadow(QFrame.Raised)

        pixmap = QPixmap("images/new.xpm")
        self.label_icon = QLabel(self.window_icon)
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setFixedSize(40, 50)

        self.label_title = QLabel(self.lefttop)
        self.label_title.setText("Новый проект")

        # self.label_title.setPixmap(QIcon("images/okpic.xpm"))
        self.label_title.setFixedSize(int(self.width() / 2) - 40, 50)
        self.label_title.mousePressEvent = self.mouse_press
        self.label_title.mouseMoveEvent = self.mouse_move

        self.label_title.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 10px; '
            'border: 1px solid black; '
            'border-right: none; '
            'border-left: none; '
        )

        self.window_icon.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 10px; '
            'border: 1px solid black; '
            'border-right: none; '
            'padding-right: 5px; '
            'padding-left: 5px; '
        )

        self.common_actions = QMenuBar(self.righttop)
        self.common_actions.mousePressEvent = self.mouse_press
        self.common_actions.mouseMoveEvent = self.mouse_move

        icon_hide = QIcon("images/hide.xpm")
        self.common_actions.addAction("__", self.showMinimized)
        self.common_actions.actions()[0].setIcon(icon_hide)

        self.common_actions.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 10px; '
            'border: 1px solid black; '
            'border-left: none;'
        )

        self.common_actions.setFixedSize(int(self.width() / 2), 50)

        self.hbox.addWidget(self.window_icon)
        self.hbox.addWidget(self.lefttop)
        self.hbox.addWidget(self.righttop)

        self.lbl = QLabel("Выберите размер рабочей области:")

        self.combo = QComboBox()
        self.combo.addItem("2x2 (4)")
        self.combo.addItem("3x3 (9)")
        self.combo.addItem("4x4 (16)")
        self.combo.addItem("5x5 (25)")
        # self.combo.addItem("6x6 (36)")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.lbl)
        hlayout.addWidget(self.combo)
        # hlayout.addStretch(1)

        # pixmap = QPixmap("images/dividev2.png")
        self.btn_ok = QPushButton("ОК")
        self.btn_ok.setIcon(QIcon("images/okpic.xpm"))
        self.btn_close = QPushButton("Закрыть")
        # self.btn_close.setStyleSheet("background-color: #e24f5f;")
        self.btn_close.setIcon(QIcon("images/closepic.xpm"))

        descr = QTextEdit(
            """
            Описание Описание Описание Описание Описание Описание
            Описание Описание Описание Описание Описание Описание
            Описание Описание Описание Описание Описание Описание
            Описание Описание Описание Описание Описание Описание
            """
        )
        descr.setReadOnly(True)

        vlayout = QVBoxLayout(self.bottom)
        # vlayout.setAlignment(Qt.AlignTop)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(descr)

        hlayout_2 = QHBoxLayout()
        hlayout_2.addStretch(1)
        hlayout_2.addWidget(self.btn_ok)
        hlayout_2.addWidget(self.btn_close)

        vlayout.addLayout(hlayout_2)

        self.bottom.setFixedSize(self.width(), self.height() - 50)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.bottom)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.main_widget.setLayout(self.vbox)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.setWindowIcon(QtGui.QIcon("images/smile.ico"))

    def mouse_press(self, event):
        if self.width() / 2 - 50 < event.scenePosition().x() < self.width() / 2 + 50:
            self.click_position = event.globalPosition().toPoint()
        if event.scenePosition().x() > self.width() / 2:
            QMenuBar.mousePressEvent(self.common_actions, event)
        else:
            QLabel.mousePressEvent(self.label_title, event)

    def mouse_move(self, event):
        if not self.isFullScreen():
            if self.width() / 2 - 50 < event.scenePosition().x() < self.width() / 2 + 50:
                if event.buttons() == Qt.LeftButton:
                    new_pos = self.pos() + event.globalPosition().toPoint() - self.click_position
                    self.move(new_pos)
                    self.click_position = event.globalPosition().toPoint()
        if event.scenePosition().x() > self.width() / 2:
            QMenuBar.mouseMoveEvent(self.common_actions, event)
        else:
            QLabel.mouseMoveEvent(self.label_title, event)


# app = QApplication(sys.argv)
# ex = OnLoadSetuper()
# ex.show()
# sys.exit(app.exec())
