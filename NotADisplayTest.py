import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import *

from functools import partial
from random import randint

from PyQt5.uic import loadUi

GlLoginHash, GlPassHash = 123, 123
GlLogin = "GlLogin"


def Request_Files(l, p):
    print("Requesting files")

def Upload_File(self, l, p):
    print("Uploading file")
class MainMenu(QMainWindow):
    def UploadFile(self):
       try:
           Upload_File(GlLoginHash, GlPassHash)
       except:
           print("Something went wrong")

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi("MainMenuUI.ui", self)
        self.NameLabel.setText("NAME : " + GlLogin)
        self.UploadButton.clicked.connect(self.UploadFile)
        self.RefreshButton.clicked.connect(self.newData)

        #self.gridLayout = QGridLayout(self)
        #self.gridLayout.addWidget(QPushButton("Get new data", clicked=self.newData), 0, 1)
        data = self.createDate()
        self.DisplayFiles(data)



    def DownloadFile(self, l, p, f):
        print("Downloading file")
    def createDate(self):
        numberOfButtons = randint(2, 11)
        print(numberOfButtons)
        data = '|'.join(["fileName{}.png".format(i) for i in range(0, numberOfButtons)])
        return data

    def newData(self):
        numberOfButtons = randint(2, 11)
        data = '|'.join(["fileName{}.png".format(i) for i in range(0, numberOfButtons)])
        countLayout = self.gridLayout.count()
        if countLayout > 1:
            for it in range(countLayout - 1):
                w = self.gridLayout.itemAt(1).widget()
                self.gridLayout.removeWidget(w)
                w.hide()
        self.DisplayFiles(self.createDate())

    def RefreshFiles(self):
        self.DisplayFiles(Request_Files(GlLoginHash, GlPassHash))

    def DisplayFiles(self, data):
        print("Displaying files")
        print("BEFORE CUT :" + str(data))
        data = data.split("|")[:len(data.split("|"))]
        print("AFTER CUT :" + str(data))# - 1]
        buttons = {}
        j, index, prev = 0, 0, 0
        for i in range(0, len(data)):
            if i % 3 == 0:
                j += 1
                index = 0
            index += 1
            buttons[(index, j)] = QPushButton(str(data[prev]))
            prev += 1
            print("Files displayed")
            pixmap = QPixmap("Ok.png")

            # scriptDir = path.dirname(path.realpath(__file__))
            # self.setWindowIcon(QtGui.QIcon(scriptDir + path.sep + 'button.png'))

            #            print("SYS : + " + (data[prev - 1])[len(str(data[prev - 1])) - len(".mp3"):])

            if ((data[prev - 1])[len(str(data[prev - 1])) - len(".mp3"):] == ".mp3"):
                buttons[(index, j)].setIcon(QIcon('MP3icon.jpg'))
            elif ((data[prev - 1])[len(str(data[prev - 1])) - len(".png"):] == ".png"):
                buttons[(index, j)].setIcon(QIcon('PNGicon.png'))
            elif ((data[prev - 1])[len(str(data[prev - 1])) - len(".html"):] == ".html"):
                buttons[(index, j)].setIcon(QIcon('HTMLicon.jpg'))
                # buttons[(index, j)].setIconSize()

            buttons[(index, j)].clicked.connect(
                #                partial(DownloadFile, str(window.LoginHash), str(window.PassHash), str(data[prev - 1])))
                partial(self.DownloadFile, str("window.LoginHash"),
                        str("window.PassHash"),
                        str(data[prev - 1])))

            buttons[(index, j)].setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred)
            self.gridLayout.addWidget(buttons[(index, j)], index, j)

    def Show(self):
        print("Global login is supposed to be " + GlLogin)
        self.ui.NameLabel.setText("NAME : " + GlLogin)
        self.ui.show()

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(QPushButton("Get new data", clicked=self.newData), 0, 1)

        data = self.createDate()
        self.DisplayFiles(data)

    def DownloadFile(self, LoginHash, PassHash, Filename):
        print("FILE : "+ str(Filename))

    def DisplayFiles(self, data):
        print("Displaying files")
        data = data.split("|")[:len(data.split("|"))] # - 1]
        buttons = {}
        j, index, prev = 0, 0, 0
        for i in range(0, len(data)):
            if i % 3 == 0:
                j += 1
                index = 0
            index += 1
            buttons[(index, j)] = QPushButton(str(data[prev]))
            prev += 1
            pixmap = QPixmap("Ok.png")

            # scriptDir = path.dirname(path.realpath(__file__))
            # self.setWindowIcon(QtGui.QIcon(scriptDir + path.sep + 'button.png'))

#            print("SYS : + " + (data[prev - 1])[len(str(data[prev - 1])) - len(".mp3"):])

            if ((data[prev - 1])[len(str(data[prev - 1])) - len(".mp3"):] == ".mp3"):
                buttons[(index, j)].setIcon(QIcon('MP3icon.jpg'))
            elif ((data[prev - 1])[len(str(data[prev - 1])) - len(".png"):] == ".png"):
                buttons[(index, j)].setIcon(QIcon('PNGicon.png'))
            elif ((data[prev - 1])[len(str(data[prev - 1])) - len(".html"):] == ".html"):
                buttons[(index, j)].setIcon(QIcon('HTMLicon.jpg'))
                # buttons[(index, j)].setIconSize()

            buttons[(index, j)].clicked.connect(
#                partial(DownloadFile, str(window.LoginHash), str(window.PassHash), str(data[prev - 1])))
                partial(self.DownloadFile, str("window.LoginHash"),
                                           str("window.PassHash"),
                                           str(data[prev - 1])))

            buttons[(index, j)].setSizePolicy(
                                                QSizePolicy.Preferred,
                                                QSizePolicy.Preferred)
            self.gridLayout.addWidget(buttons[(index, j)], index, j)

    def createDate(self):
        numberOfButtons = randint(2, 11)
        data = '|'.join([ "fileName{}.png".format(i) for i in range(1, numberOfButtons) ])
        return data

    def newData(self,data):
        countLayout = self.gridLayout().count()
        if countLayout > 1:
            for it in range(countLayout - 1):
                w = self.gridLayout.itemAt(1).widget()
                self.gridLayout.removeWidget(w)
                w.hide()
        self.DisplayFiles(self.createDate())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mm = MainMenu()
    mm.Show()
    sys.exit(app.exec_())