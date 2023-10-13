#!/usr/bin/python

"""
ZetCode PySide tutorial
This example shows a QtGui.QCalendarWidget widget.

author: Jan Bodnar
website: zetcode.com
"""

import sys
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QWidget, QCalendarWidget, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QPushButton


class CalendarDT(QWidget):

    def __init__(self, parent):
        super(CalendarDT, self).__init__()

        self.parent = parent
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked.connect(self.show_date)

        self.lbl = QLabel(self)
        self.date = self.cal.selectedDate()
        self.lbl.setText(self.date.toString("dd.MM.yy"))

        ok_btn = QPushButton("Выбрать")
        ok_btn.clicked.connect(self.save_date)

        self.setWindowTitle('Выбор даты')
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        hlayout.addWidget(self.lbl)
        hlayout.addWidget(ok_btn)

        vlayout.addWidget(self.cal)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

    def show_date(self, date):
        self.lbl.setText(date.toString("dd.MM.yy"))

    def save_date(self):
        self.parent.date = self.cal.selectedDate()
        self.parent.date_line_edit.setText(self.parent.date.toString("dd.MM.yy"))
        self.close()


# app = QApplication(sys.argv)
# ex = CalendarDT()
# ex.show()
# sys.exit(app.exec())
