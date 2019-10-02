from sys import argv
from functools import partial
from os import system
from PyQt5.QtWidgets import QFileDialog
import base64
from socket import AF_INET, socket, SOCK_STREAM
import threading
from hashlib import md5
from pathlib import Path
import pbkdf2
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtCore import pyqtSlot, QParallelAnimationGroup, QPropertyAnimation, QPoint, QAnimationGroup
from PyQt5.uic import loadUi


""" col col col
    row row row
    row row row
    row row row
"""
buttons = {}
gridLayout = QGridLayout();
widget = QWidget();
app = QApplication(argv)
def PrintNumber(i, j):
    print("You have clicked NotAButton with NotANumber (%d, %d)" %(i, j))


def DisplayFiles(data):
    app =QApplication(argv);
    print("Displaying files")

    def Download(Filename):
        print("Ready to download %s" % Filename)

    print(data)
    data = data.split("|")[:len(data.split("|")) - 1]
    buttons = {}
    j, index, prev = 0, 0, 0
    for i in range(0, len(data)):

        if i % 3 == 0:
            j += 1
            index = 0
        index += 1
        buttons[(index, j)] = QPushButton(str(data[prev]))
        prev += 1
        buttons[(index, j)].clicked.connect(partial(Download, str(data[prev - 1])))
        gridLayout.addWidget(buttons[(index, j)], index, j)
        app.exec_()

DisplayFiles(data = "R|NotAFile|MaybeAFile|100%AFile|123|123|123|1132|123")