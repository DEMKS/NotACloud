"""The main executable file of the NAC desktop client v 0.1.3"""
import base64
import pbkdf2
import threading
from sys import argv
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.uic import loadUi
from functools import partial
from os import makedirs, path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon, QFont
from socket import AF_INET, socket, SOCK_STREAM
from PyQt5.QtCore import QParallelAnimationGroup, QPropertyAnimation, QPoint, QAnimationGroup
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QGridLayout, \
    QFileDialog, QSizePolicy, QDialog, QWidget, QLabel, QHBoxLayout, QVBoxLayout

# Global variables declaration
BUFFISZE = 5120 * 1024 * 2
GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH = '', '', '', ''
host_ip, server_port = "127.0.0.1", 7557
ButtonStyleSheet = "background-color:#CFB3CD;" \
                   "border-radius: 15px;"
ApplicationStyleSheet = "background-color:#ACBED8;"
ButtonStyleSheet = ""
ApplicationStyleSheet = ""


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


class LoginWindow(QMainWindow):
    """The login window class"""

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi("UI/LoginWindow.ui", self)
        self.setStyleSheet(ApplicationStyleSheet)
        self.NotAButton.clicked.connect(self.NotAButtonClicked)

    def NotAButtonClicked(self):
        global GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH
        if Path("./Cached.NAC").is_file():
            print("Found login and password file, executing corresponding instructions....")
            file = open("./Cached.NAC", "r")
            # could be optimized with "with" keyword
            GLLOGINHASH = str(file.readline())
            GLLOGINHASH = GLLOGINHASH[:len(GLLOGINHASH) - 1]
            GLPASSHASH = str(file.readline())
            print(GLPASSHASH)
            print(GLLOGINHASH)
            self.loginHash = GLLOGINHASH
            self.PassHash = GLPASSHASH
            file = open("./login.NAC", "r")
            GLLOGIN = str(file.readline())
            print("login : " + GLLOGIN)
            print("login hash: " + GLLOGINHASH)
            try:
                if Send_login(login=GLLOGINHASH, Pass=GLPASSHASH, Raw=True):
                    print("login succeed, continuing execution")
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


class DragNDropButton(QPushButton):
    """Button class but with drag 'n drop"""

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        text = e.mimeData().text()
        if "file:///" in text and not e.mimeData().hasFormat("text/plain"):
            self.path = text[8:]
            print(text[8:])

        # e.accept() e.ignore()
        e.accept()

    def dropEvent(self, e):
        Upload_file(ByPath=True, filepath=self.path)
        print(GLLOGINHASH)
        print("EVENT ACCEPTED")


class TextEditor(QMainWindow):
    """Text editor class"""

    def __init__(self, Filename):
        QMainWindow.__init__(self)
        self.ui = loadUi("UI/TextEditor.ui", self)
        self.Filename = "Downloads/" + Filename
        DownloadFile(GLLOGINHASH, GLPASSHASH, Filename)
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
            UpdateFile(login=GLLOGINHASH, Pass=GLPASSHASH, Filename=self.Filename)

    def Show(self):
        self.ui.show()


class SubWindow(QMainWindow):
    """Subwindow class is used for authorisation"""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setStyleSheet(ApplicationStyleSheet)
        self.ui = loadUi("UI/SubWindow.ui", self)
        thr.window.show()
        self.UploadButton.clicked.connect(self.UploadButtonClicked)

    def UploadButtonClicked(self):
        global GLLOGINHASH, GLPASSHASH
        print("Upload button clicked")
        if Send_login(self.LoginText.text(), self.PassText.text()):
            GLLOGINHASH = pbkdf2.crypt(self.LoginText.text(), salt="NotASalt", iterations=150)
            GLPASSHASH = pbkdf2.crypt(self.PassText.text(), salt="NotASalt", iterations=150)
            self.ui.hide()
            thr.mainmenu.Show()
        else:
            print("Something went wrong")

    def Show(self):
        print("Initiating animation")
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
        print("Aniamtion initiated")
        self.ui.show()

    def Hide(self):
        self.ui.hide()


class MainMenu(QMainWindow):
    """The main menu class"""

    def __init__(self):
        QMainWindow.__init__(self)
        parentwdg = QWidget()
        self.gridLayout = QGridLayout(parentwdg)
        self.ui = loadUi("UI/MainMenuUI.ui", self)
        self.NameLabel.setText("NAME : " + GLLOGIN)
        self.UploadButton = DragNDropButton("UPLOAD", self)
        self.UploadButton.move(160, 0)
        self.UploadButton.resize(121, 71)
        self.UploadButton.setFont(QFont("Bungee inline", 9))
        self.setAutoFillBackground(True)
        self.ui.setStyleSheet(ApplicationStyleSheet)
        self.UploadButton.clicked.connect(OpenUploadThread)
        self.RefreshButton.clicked.connect(self.RefreshFiles)

    def RefreshFiles(self):
        self.newData(Request_Files(GLLOGINHASH, GLPASSHASH))

    def newData(self, data):
        print("New data called")
        if data == '':
            if self.gridLayout.count() > 1:
                w = self.gridLayout.itemAt(0).widget()
                self.gridLayout.removeWidget(w)
                w.hide()
        else:
            print("new data else reached")
            countLayout = self.gridLayout.count()
            if countLayout > 1:
                while self.gridLayout.count():
                    child = self.gridLayout.takeAt(0)
            print("new data else executed correctly")
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
            if data[prev - 1].split(".")[1:][0] == "mp3":
                img = "MP3icon.jpg"
            elif data[prev - 1].split(".")[1:][0] == "png":
                img = "PNGicon.png"
            elif data[prev - 1].split(".")[1:][0] == "html":
                img = "HTMLicon.jpg"
            Filename = str(data[prev])
            actions = {"edit": partial(Edit_File, Filename),
                       "delete": partial(Delete_File, GLLOGINHASH, GLPASSHASH, Filename),
                       "download": partial(DownloadFile, GLLOGINHASH, GLPASSHASH, Filename)
                       }
            buttons[(index, j)] = InitiateFileInterationButtons(Filename, actions)
            prev += 1
            self.gridLayout.addLayout(buttons[(index, j)], index, j)
            print("initiated {}".format(Filename))

    def Show(self):
        print("Global login is supposed to be " + GLLOGIN)
        self.ui.NameLabel.setText("NAME : " + GLLOGIN)
        self.RefreshFiles()
        self.ui.show()


class FileDialog(QDialog):
    """File edit delete and download dialog"""

    def __init__(self):
        QDialog.__init__(self)
        self.setStyleSheet(ApplicationStyleSheet)
        self.ui = loadUi("UI/FileDialog.ui", self)

    def Show(self, loginHash, PassHash, Filename):
        self.DeleteButton.clicked.connect(partial(Delete_File, loginHash, PassHash, Filename))
        self.DeleteButton.setStyleSheet(ButtonStyleSheet)
        self.EditButton.clicked.connect(partial(Edit_File, Filename))
        self.EditButton.setStyleSheet(ButtonStyleSheet)
        self.DownloadButton.clicked.connect(partial(DownloadFile, loginHash, PassHash, Filename))
        self.DownloadButton.setStyleSheet(ButtonStyleSheet)
        self.ui.show()


def OpenUploadThread():
    try:
        upload = UploadThread(thr.window.loginHash, thr.window.PassHash)
        upload.start()
    except:
        print("Something went wrong")


def DownloadFile(loginHash, PassHash, Filename):
    try:
        print("Download file called")
        loginHash, PassHash, Filename = str(loginHash), str(PassHash), str(Filename)
        print(f"D|{loginHash}|{PassHash}|{Filename}")
        tcp_client = socket(AF_INET, SOCK_STREAM)
        # Establish connection to TCP server and exchange data
        print("Downloading file : %s" % Filename)
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(bytes(f"D|{loginHash}|{PassHash}|{Filename}", encoding="utf8"))
        received = tcp_client.recv(BUFFISZE)
        if not Path("./Downloads/").is_dir():
            makedirs("./Downloads/")
        received = received.decode("utf8")
        received = received.split("|")[1:]
        print(str(received))
        FileBase64Dec(s=received, save_path="./Downloads/", name=Filename)
    finally:
        tcp_client.close()


def UpdateFile(login, Pass, Filename):
    try:
        print("Hello?")
        global GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH
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

        print(('U|' + str(pbkdf2.crypt(login, salt="NotASalt", iterations=150)) + '|' + str(
            pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
        print("login = " + login + "\nPass = " + Pass)
        tcp_client.sendall(bytes("U|" + str(login) + "|" + str(
            Pass) + "|", encoding="utf8") + bytes(x.split("/")[len(
            x.split("/")) - 1] + "|", encoding="utf8") + bytes(file, encoding="utf8"))
        print(path)
        received = tcp_client.recv(BUFFISZE)
        received = received.decode("utf8")
    except:
        print("Something went wrong")
    finally:
        tcp_client.close()


def FileBase64Enc(filepath):
    with open(filepath, 'rb') as image:
        FileEnc = image.readlines()
    FileEnc = map(base64.b64encode, FileEnc)
    return FileEnc


def FileBase64Dec(s, save_path, name):
    s = map(base64.b64decode, s)
    with open(save_path + name, 'wb') as file:
        for i in s:
            file.write(i)


def Upload_file(login=GLLOGINHASH, Pass=GLPASSHASH, ByPath=False, filepath=""):
    try:
        global GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH
        if login == "":
            login = GLLOGINHASH
        if Pass == "":
            Pass = GLPASSHASH
        tcp_client = socket(AF_INET, SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        if not ByPath:
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.AnyFile)
            if dlg.exec_():
                dlgpath = dlg.selectedFiles()
        else:
            dlgpath = [filepath]
        for x in dlgpath:
            fileenc = FileBase64Enc(x)
            file = ''
            for i in fileenc:
                string = str(i)[:len(str(i)) - 1]
                string = string[2:]
                file += string + '|'
            print(('U|' + str(pbkdf2.crypt(
                login, salt="NotASalt", iterations=150)) + '|' + str(
                pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
            print("Uploadlogin = " + login + "\nPass = " + Pass)
            tcp_client.sendall(bytes("U|" + str(
                login) + "|" + str(Pass) + "|", encoding="utf8") + bytes(
                x.split("/")[len(
                    x.split("/")) - 1] + "|", encoding="utf8") + bytes(file, encoding="utf8"))
        print(path)
        received = tcp_client.recv(BUFFISZE).decode("utf8")
    except:
        print("Something went wrong")
    finally:
        tcp_client.close()
    thr.mainmenu.RefreshFiles()


def Delete_File(loginHash, PassHash, Filename):
    try:
        loginHash, PassHash, Filename = str(loginHash), str(PassHash), str(Filename)
        tcp_client = socket(AF_INET, SOCK_STREAM)
        print("Deleting file : %s" % Filename)
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(bytes(f"R|{loginHash}|{PassHash}|{Filename}", encoding="utf8"))
        received = tcp_client.recv(BUFFISZE)
        received = received.decode()
        if received == "File deleted":
            print("Succeed")
        else:
            print("Something went wrong")
            print(received)
    finally:
        tcp_client.close()
    print("Deleting file " + Filename)
    thr.mainmenu.RefreshFiles()
    # We are working on this one


def Send_login(login, Pass, Raw=False):
    try:
        global GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH
        try:
            tcp_client = socket(AF_INET, SOCK_STREAM)
            tcp_client.connect((host_ip, server_port))
        except:
            tcp_client = 1
            print("Socket failure")
        if Raw:
            print("Sending raw data....")
            print(('L|' + str(login) + '|' + str(Pass)))
            tcp_client.sendall(bytes(('L|' + str(login) + '|' + str(Pass)), encoding="utf8"))
        else:
            print("Sending encrypted data")
            print(('L|' + str(pbkdf2.crypt(login, salt="NotASalt", iterations=150)) + '|' + str(
                pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))))
            tcp_client.sendall(bytes(('L|' + str(
                pbkdf2.crypt(login, salt="NotASalt", iterations=150)) + '|' + str(
                pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))), encoding="utf8"))
        received = tcp_client.recv(5120)
        received = received.decode("utf8")
        if received == "Auth succeed":
            print("Credentials are correct")
            Succeed = True
            with open("Cached.NAC", "w") as file:
                if Raw:
                    file.write(login)
                    file.write("\n")
                    file.write(Pass)
                    GLLOGINHASH, GLPASSHASH = login, Pass
                else:
                    file.write(str(pbkdf2.crypt(login, salt="NotASalt", iterations=150)))
                    file.write("\n")
                    file.write(str(pbkdf2.crypt(Pass, salt="NotASalt", iterations=150)))
                    GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH = login, Pass, str(
                        pbkdf2.crypt(login, salt="NotASalt", iterations=150)), str(
                        pbkdf2.crypt(Pass, salt="NotASalt", iterations=150))

            if not Raw:
                with open("login.NAC", "w") as file:
                    print("Not raw input detected")
                    file.write(login)
            else:
                print("Raw input detected")

        else:
            Succeed = False
            print("Either credentials are incorrect or our servers are unavailable right now")
    finally:
        tcp_client.close()
    return Succeed


def Request_Files(loginHash=GLLOGINHASH, PassHash=GLPASSHASH):
    try:
        global GLLOGIN, GLPASS, GLLOGINHASH, GLPASSHASH
        tcp_client = socket(AF_INET, SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(bytes(("C|" + loginHash + '|' + PassHash), encoding="utf8"))
        received = tcp_client.recv(BUFFISZE)
        received = received.decode("utf8")
        print("While requesting files received following response:" + received)
    except:
        print("File request returned an error")
    finally:
        tcp_client.close()
        return received


def Edit_File(Filename):
    print("This feature is still in development")
    edit = TextEditor(Filename)
    edit.Show()


class UploadThread(threading.Thread):
    """File upload (To stop the main thread from stopping)"""

    def __init__(self, loginHash, PassHash):
        threading.Thread.__init__(self)
        self.loginHash, self.PassHash = loginHash, PassHash

    def run(self):
        Upload_file(self.loginHash, self.PassHash)


class DownloadThread(threading.Thread):
    """File download thread"""

    def __init__(self, loginHash, PassHash, Filename):
        threading.Thread.__init__(self)
        self.loginHash, self.PassHash, self.Filename = loginHash, PassHash, Filename

    def run(self):
        DownloadFile(self.loginHash, self.PassHash, self.Filename)


class UIThread(threading.Thread):
    """User interface thread"""

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app = QApplication(argv)
        self.window = LoginWindow()
        print("MAIN WIDNOW DONE")
        self.mainmenu = MainMenu()
        print("MAIN MENU DONE")
        self.window.Show()
        print("WINDOW SHOW")
        self.subwindow = SubWindow()
        print("SUBWINDOW INITIALAISED")
        app.exec_()


thr = UIThread()
thr.start()
