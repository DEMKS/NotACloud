from sys import argv
import random
from os import system, makedirs, path
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog, QSizePolicy, QDialog, QTextEdit
import base64
from socket import AF_INET, socket, SOCK_STREAM
import threading
from pathlib import Path
import pbkdf2
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout
from PyQt5.QtCore import pyqtSlot, QParallelAnimationGroup, QPropertyAnimation, QPoint, QAnimationGroup, QSize
from PyQt5.uic import loadUi

# Main variation , GLVars
BUFFISZE = 5120 * 1024 * 2
global GlLogin, GlPass, GlLoginHash, GlPassHash
GlLogin, GlPass, GlLoginHash, GlPassHash = '', '', '', ''


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi("UI/NotAUI.ui", self)
        self.NotAButton.clicked.connect(self.NotAButtonClicked)

    def NotAButtonClicked(self):
        global GlLogin, GlPass, GlLoginHash, GlPassHash
        file = Path("./Cached.NAC")
        if file.is_file():
            print("Found login and password file, executing corresponding instructions....")
            file = open("./Cached.NAC", "r")
            # could be optimized with "with" keyword
            GlLoginHash = str(file.readline())
            GlLoginHash = GlLoginHash[:len(GlLoginHash) - 1]
            GlPassHash = str(file.readline())
            print(GlPassHash)
            print(GlLoginHash)
            self.LoginHash = GlLoginHash
            self.PassHash = GlPassHash
            file = open("./Login.NAC", "r")
            GlLogin = str(file.readline())
            print("Login : " + GlLogin)
            print("Login hash: " + GlLoginHash)
            try:
                if Send_login(Login=GlLoginHash, Pass=GlPassHash, Raw=True):
                    print("Login succeed, continuing execution")
                    self.ui.hide()
                    thr.mainmenu.Show()
                else:
                    self.ui.hide()
                    thr.subwindow.Show()
            except:
                print("Something went wrong")
        else:
            thr.subwindow.Show()

    def Show(self):
        self.ui.show()

    def Hide(self):
        self.ui.hide()


class TextEditor(QMainWindow):
    def __init__(self, Filename):
        QMainWindow.__init__(self)
        self.ui = loadUi("UI/TextEditor.ui", self)
        self.Filename = "Downloads/" + Filename
        DownloadFile(GlLoginHash, GlPassHash, Filename)
        try:
            print(open("Downloads/" + str(Filename)).read())
            self.textedit.setText(str(open("Downloads/" + str(Filename)).read()))
        except:
            print("Something went wrong")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_S:
            print("S IS PRESSED")
            print(self.textedit.toPlainText())
            open(self.Filename, "w+").write(self.textedit.toPlainText())
            UpdateFile(Login=GlLoginHash, Pass=GlPassHash, Filename=self.Filename)

    def Show(self):
        self.ui.show()


class SubWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi("UI/SubWindow.ui", self)
        thr.window.show()
        self.UploadButton.clicked.connect(self.UploadButtonClicked)

    def UploadButtonClicked(self):
        if Send_login(self.LoginText.text(), self.PassText.text()):
            self.WIN.__init__()
            self.ui.hide()
            self.MAINMEN.Show()

    def Show(self):
        animation_group = QParallelAnimationGroup(self)
        for w in (self.LoginText, self.UploadButton, self.PassText):
            start_pos = w.pos()
            end_pos = w.pos() + QPoint(0, -250)
            animation = QPropertyAnimation(
                self,
                propertyName=b"pos",
                targetObject=w,
                startValue=start_pos,
                endValue=end_pos,
                duration=900,
            )
            animation_group.addAnimation(animation)
        animation_group.start(QAnimationGroup.DeleteWhenStopped)
        self.ui.show()

    def Hide(self):
        self.ui.hide()


class MainMenu(QMainWindow):
    def UploadFile(self):
        try:
            upload = UploadThread(thr.window.LoginHash, thr.window.PassHash)
            upload.run()
        except:
            print("Something went wrong")

    def __init__(self):
        QMainWindow.__init__(self)
        self.gridLayout = QGridLayout(self)
        self.ui = loadUi("UI/MainMenuUI.ui", self)
        self.NameLabel.setText("NAME : " + GlLogin)
        self.UploadButton.clicked.connect(self.UploadFile)
        self.RefreshButton.clicked.connect(self.RefreshFiles)

    def RefreshFiles(self):
        self.newData(Request_Files(GlLoginHash, GlPassHash))

    def newData(self, data):
        if data == '':
            if self.gridLayout.count() > 1:
                w = self.gridLayout.itemAt(0).widget()
                self.gridLayout.removeWidget(w)
                w.hide()
        else:
            countLayout = self.gridLayout.count()
            if countLayout > 1:
                for it in range(countLayout - 1):
                    w = self.gridLayout.itemAt(1).widget()
                    self.gridLayout.removeWidget(w)
                    w.hide()
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
            buttons[(index, j)] = QPushButton(str(data[prev]))
            prev += 1
            print("SYS : + " + (data[prev - 1])[len(str(data[prev - 1])) - len(".mp3"):])
            if (data[prev - 1])[len(str(data[prev - 1])) - len(".mp3"):] == ".mp3":
                buttons[(index, j)].setIcon(QIcon('MP3icon.jpg'))
            elif (data[prev - 1])[len(str(data[prev - 1])) - len(".png"):] == ".png":
                buttons[(index, j)].setIcon(QIcon('PNGicon.png'))
            elif (data[prev - 1])[len(str(data[prev - 1])) - len(".html"):] == ".html":
                buttons[(index, j)].setIcon(QIcon('HTMLicon.jpg'))
            buttons[(index, j)].clicked.connect(
                partial(FileDialog().Show, str(thr.window.LoginHash), str(thr.window.PassHash), str(data[prev - 1])))
            buttons[(index, j)].setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred)
            thr.mainmenu.gridLayout.addWidget(buttons[(index, j)], index, j)

    def Show(self):
        print("Global login is supposed to be " + GlLogin)
        self.ui.NameLabel.setText("NAME : " + GlLogin)
        self.RefreshFiles()
        self.ui.show()


class FileDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = loadUi("UI/FileDialog.ui", self)

    def Show(self, LoginHash, PassHash, Filename):
        self.DeleteButton.clicked.connect(partial(Delete_File, LoginHash, PassHash, Filename))
        self.EditButton.clicked.connect(partial(Edit_File, LoginHash, PassHash, Filename, self))
        self.DownloadButton.clicked.connect(partial(DownloadFile, LoginHash, PassHash, Filename))
        self.ui.show()


def DownloadFile(LoginHash, PassHash, Filename):
    try:
        print("Download file called")
        LoginHash, PassHash, Filename = str(LoginHash), str(PassHash), str(Filename)
        print(f"D|{LoginHash}|{PassHash}|{Filename}")
        tcp_client = socket(AF_INET, SOCK_STREAM)
        # Establish connection to TCP server and exchange data
        print("Downloading file : %s" % Filename)
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(bytes(f"D|{LoginHash}|{PassHash}|{Filename}", encoding="utf8"))
        received = tcp_client.recv(BUFFISZE)
        if not (Path("./Downloads/").is_dir()):
            makedirs("./Downloads/")
        received = received.decode("utf8")
        received = received.split("|")[1:]
        print(str(received))
        FileBase64Dec(s=received, save_path="./Downloads/", name=Filename)
    finally:
        tcp_client.close()


def UpdateFile(Login, Pass, Filename):
    try:
        print("Hello?")
        global GlLogin, GlPass, GlLoginHash, GlPassHash
        tcp_client = socket(AF_INET, SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        x = Filename
        fileenc = FileBase64Enc(x)
        file = ''
        print(fileenc)
        for i in fileenc:
            string = str(i)[:len(str(i)) - 1]
            string = string[2:]
            file += string + '|'

        print(('U|' + str(pbkdf2.crypt(Login, salt="NotASalt", iterations=150)) + '|' + str(
            pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
        print("Login = " + Login + "\nPass = " + Pass)
        tcp_client.sendall(bytes("U|" + str(Login) + "|" + str(Pass) + "|", encoding="utf8") + bytes(
            x.split("/")[len(x.split("/")) - 1] + "|", encoding="utf8") + bytes(file, encoding="utf8"))
        print(path)
        received = tcp_client.recv(BUFFISZE)
        received = received.decode("utf8")
    except:
        print("Something went wrong")
    finally:
        tcp_client.close()


def FileBase64Enc(path):
    with open(path, 'rb') as image:
        FileEnc = image.readlines()
    FileEnc = map(base64.b64encode, FileEnc)
    return FileEnc


def FileBase64Dec(s, save_path, name):
    s = map(base64.b64decode, s)
    with open(save_path + name, 'wb') as file:
        for i in s:
            file.write(i)


host_ip, server_port = "185.181.8.21", 7557


def Upload_File(Login=GlLoginHash, Pass=GlPassHash):
    try:
        global GlLogin, GlPass, GlLoginHash, GlPassHash
        tcp_client = socket(AF_INET, SOCK_STREAM)
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        tcp_client.connect((host_ip, server_port))
        if dlg.exec_():
            path = dlg.selectedFiles()
        for x in path:
            fileenc = FileBase64Enc(x)
            file = ''
            for i in fileenc:
                string = str(i)[:len(str(i)) - 1]
                string = string[2:]
                file += string + '|'
            print(('U|' + str(pbkdf2.crypt(Login, salt="NotASalt", iterations=150)) + '|' + str(
                pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
            print("Login = " + Login + "\nPass = " + Pass)
            tcp_client.sendall(bytes("U|" + str(Login) + "|" + str(Pass) + "|", encoding="utf8") + bytes(
                x.split("/")[len(x.split("/")) - 1] + "|", encoding="utf8") + bytes(file, encoding="utf8"))
        print(path)
        received = tcp_client.recv(BUFFISZE)
        received = received.decode("utf8")
    except:
        print("Something went wrong")
    finally:
        tcp_client.close()


def Delete_File(LoginHash, PassHash, Filename):
    try:
        LoginHash, PassHash, Filename = str(LoginHash), str(PassHash), str(Filename)
        tcp_client = socket(AF_INET, SOCK_STREAM)
        print("Deleting file : %s" % Filename)
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(bytes(f"R|{LoginHash}|{PassHash}|{Filename}", encoding="utf8"))
        received = tcp_client.recv(BUFFISZE)
        received = received.decode()
        if received == "File deleted":
            print("Succeed")
        else:
            print("Something went wrong")
    finally:
        tcp_client.close()
    print("Deleting file " + Filename)
    # We are working on this one


def Send_login(Login, Pass, Raw=False):
    try:
        global GlLogin, GlPass, GlLoginHash, GlPassHash
        tcp_client = socket(AF_INET, SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        if Raw:
            print("Sending raw data....")
            print(('L|' + str(Login) + '|' + str(Pass)))
            tcp_client.sendall(bytes(('L|' + str(Login) + '|' + str(Pass)), encoding="utf8"))
        else:
            print("Sending encrypted data")
            print(('L|' + str(pbkdf2.crypt(Login, salt="NotASalt", iterations=150)) + '|' + str(
                pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
            tcp_client.sendall(bytes(('L|' + str(pbkdf2.crypt(Login, salt="NotASalt", iterations=150)) + '|' + str(
                pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))), encoding="utf8"))
        received = tcp_client.recv(5120)
        received = received.decode("utf8")
        if received == "Auth succeed":
            print("Credentials are correct")
            Succeed = True

            with open("Cached.NAC", "w") as file:
                if Raw:
                    file.write(Login)
                    file.write("\n")
                    file.write(Pass)
                    GlLoginHash, GlPassHash = Login, Pass
                else:
                    file.write(str(pbkdf2.crypt(Login, salt="NotASalt", iterations=150)))
                    file.write("\n")
                    file.write(str(pbkdf2.crypt(Pass, salt="NotASalt", iterations=150)))
                    GlLogin, GlPass, GlLoginHash, GlPassHash = Login, Pass, str(
                        pbkdf2.crypt(Login, salt="NotASalt", iterations=150)), str(
                        pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))

            if not Raw:
                with open("Login.NAC", "w") as file:
                    print("Not raw input detected")
                    file.write(Login)
            else:
                print("Raw input detected")

        else:
            Succeed = False
            print("Either credentials are incorrect or our servers are unavailable right now")
    finally:
        tcp_client.close()
    return Succeed


def Request_Files(LoginHash=GlLoginHash, PassHash=GlPassHash):
    try:
        global GlLogin, GlPass, GlLoginHash, GlPassHash
        tcp_client = socket(AF_INET, SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(bytes(("C|" + LoginHash + '|' + PassHash), encoding="utf8"))
        received = tcp_client.recv(BUFFISZE)
        received = received.decode("utf8")

        print("While requesting files received following response:" + received)
    finally:
        tcp_client.close()
        return received


def Edit_File(LoginHash, PassHash, Filename, obj):
    print("This feature is still in development")  # We are working on this one
    obj.hide()
    edit = TextEditor(Filename)
    edit.Show()


class UploadThread(threading.Thread):
    def __init__(self, LoginHash, PassHash):
        threading.Thread.__init__(self)
        self.LoginHash, self.PassHash = LoginHash, PassHash

    def run(self):
        def Upload_File(Login=GlLoginHash, Pass=GlPassHash):
            try:
                global GlLogin, GlPass, GlLoginHash, GlPassHash
                tcp_client = socket(AF_INET, SOCK_STREAM)
                dlg = QFileDialog()
                dlg.setFileMode(QFileDialog.AnyFile)
                tcp_client.connect((host_ip, server_port))
                if dlg.exec_():
                    path = dlg.selectedFiles()
                for x in path:
                    fileenc = FileBase64Enc(x)
                    file = ''
                    for i in fileenc:
                        string = str(i)[:len(str(i)) - 1]
                        string = string[2:]
                        file += string + '|'
                    print(('U|' + str(pbkdf2.crypt(Login, salt="NotASalt", iterations=150)) + '|' + str(
                        pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
                    print("Login = " + Login + "\nPass = " + Pass)
                    tcp_client.sendall(bytes("U|" + str(Login) + "|" + str(Pass) + "|", encoding="utf8") + bytes(
                        x.split("/")[len(x.split("/")) - 1] + "|", encoding="utf8") + bytes(file, encoding="utf8"))
                print(path)
                received = tcp_client.recv(BUFFISZE)
                received = received.decode("utf8")
            except:
                print("Something went wrong")
            finally:
                tcp_client.close()

        Upload_File(self.LoginHash, self.PassHash)


class DownloadThread(threading.Thread):
    def __init__(self, LoginHash, PassHash, Filename):
        threading.Thread.__init__(self)
        self.LoginHash, self.PassHash, self.Filename = LoginHash, PassHash, Filename

    def run(self):
        def DownloadFile(LoginHash, PassHash, Filename):
            try:
                print("Download file called")
                LoginHash, PassHash, Filename = str(LoginHash), str(PassHash), str(Filename)
                print(f"D|{LoginHash}|{PassHash}|{Filename}")
                tcp_client = socket(AF_INET, SOCK_STREAM)
                print("Downloading file : %s" % Filename)
                tcp_client.connect((host_ip, server_port))
                tcp_client.sendall(bytes(f"D|{LoginHash}|{PassHash}|{Filename}", encoding="utf8"))
                received = tcp_client.recv(BUFFISZE)
                if not (Path("./Downloads/").is_dir()):
                    makedirs("./Downloads/")
                received = received.decode("utf8")
                received = received.split("|")[1:]
                print(str(received))
                FileBase64Dec(s=received, save_path="./Downloads/", name=Filename)
            finally:
                tcp_client.close()

        DownloadFile(self.LoginHash, self.PassHash, self.Filename)


class UIThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app = QApplication(argv)
        self.window = MainWindow()
        print("MAIN WIDNOW DONE")
        self.mainmenu = MainMenu()
        print("MAIN MENU DONE")
        self.window.Show()
        print("WINDOW SHOW")
        self.subwindow = SubWindow()
        print("SUBWINDOW INITIALAISED")
        app.exec_()


thr = UIThread()
thr.run()
