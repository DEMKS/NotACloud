from functools import partial
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QGridLayout, QLabel, QVBoxLayout


class MainMenu(QMainWindow):
    """The main menu class"""

    def __init__(self):
        QMainWindow.__init__(self)
        self.gridLayout = QGridLayout(self)
        self.ui = loadUi("UI/MainMenuUI.ui", self)
        self.NameLabel.setText("NAME : NAME")
        self.setAutoFillBackground(True)
        self.RefreshButton.clicked.connect(self.RefreshFiles)

    def RefreshFiles(self):
        self.newData("FILE|FILE|fIlE|")

    def newData(self, data):
        print("New data called")
        if data == '':
            if self.gridLayout.count() > 1:
                w = self.gridLayout.itemAt(0).widget()
                self.gridLayout.removeWidget(w)
                w.hide()
        else:
            print("else")
            if self.gridLayout.count() > 1:
                w = self.gridLayout.itemAt(0)
                self.gridLayout.removeWidget(w)
            self.DisplayFiles(data)

    def DisplayFiles(self, data):
        print("Displaying files")
        print(data)
        data = data.split("|")[:len(data.split("|")) - 1]
        buttons = {}
        j, index, prev = 0, 0, 0
        for i in range(0, len(data)):
            if i % 3 == 0:
                j += 1
                index = 0
            index += 1
            img = "unknown.png"
            filename = str(data[prev])
            actions = {"edit": partial(print, filename),
                       "delete": partial(print, filename),
                       "download": partial(print, filename)
                       }

            def InitiateFileInterationButtons(name, actions):
                """Initiation of file interaction menu (actions is an dictionary)"""
                layout = QVBoxLayout()
                pxmp = QPixmap("unknown.png")
                lbl = QLabel()
                textlbl = QLabel(name)
                lbl.setPixmap(pxmp)
                lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                layout.addWidget(textlbl)
                layout.addWidget(lbl)
                sublayout = QHBoxLayout()
                deletebutton = QPushButton("delete")
                deletebutton.clicked.connect(actions["delete"])
                editbutton = QPushButton("edit")
                editbutton.clicked.connect(actions["edit"])
                downloadbutton = QPushButton("download")
                downloadbutton.clicked.connect(actions["download"])
                sublayout.addWidget(deletebutton)
                sublayout.addWidget(editbutton)
                sublayout.addWidget(downloadbutton)
                layout.addLayout(sublayout)
                return layout

            buttons[(index, j)] = InitiateFileInterationButtons(
                filename, actions)
            prev += 1
            self.gridLayout.addLayout(buttons[(index, j)], index, j)
            print("initiated {}".format(filename))

    def Show(self):
        self.ui.NameLabel.setText("NAME : NAME")
        self.RefreshFiles()
        self.ui.show()

app = QApplication([])
mainmenu = MainMenu()
mainmenu.Show()
app.exec_()