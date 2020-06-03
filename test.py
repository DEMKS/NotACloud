from functools import partial

from PyQt5.QtWidgets import QVBoxLayout, QApplication

from NotAFile import DownloadFile, Send_login, Request_Files, InitiateFileInterationButtons, Upload_file, UpdateFile, \
    Delete_File


def test_DownloadFile():
    DownloadFile("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                 "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", "file.txt")
    assert open("Downloads/file.txt").read() == open(
        "Uploads/$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K/file.txt").read()


def test_Send_login():
    assert Send_login("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                      "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", True) == True


def test_Request_Files():
    assert Request_Files("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                         "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v") == "123.txt|Cached.NAC|calculator.ui" \
                                                                                  "|file.txt|"


def test_InitiateFileInterationButtons():
    actions = {"edit": partial(print, 1),
               "delete": partial(print, 1),
               "download": partial(print, 1)
               }
    assert InitiateFileInterationButtons("file", actions) != QVBoxLayout()
    assert type(InitiateFileInterationButtons("file", actions)) == type(QVBoxLayout())


def test_Upload_file():
    Upload_file("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", True, "123.txt")
    assert open("123.txt").read() == open("Uploads/$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K/123.txt").read()
    assert "123.txt" in Request_Files("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                                      "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v")


def test_UpdateFile():
    Upload_file("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", True, "123.txt")
    open("123.txt", "w").write("test")
    UpdateFile("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
               "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", "123.txt")
    DownloadFile("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                 "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", "123.txt")
    assert open("Downloads/123.txt").read() == "test"


def test_Delete_File():
    Upload_file("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", True, "123.txt")
    Delete_File("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", "123.txt")
    assert "123.txt" not in Request_Files("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                                          "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v")
    Upload_file("$p5k2$96$NotASalt$RHBdqoCUFN9jUV2GhXt09xYowTs7xE9K",
                "$p5k2$96$NotASalt$SMDjJRr2CnlskoBvTJDiIqjgvKKJ4d5v", True, "123.txt")


if __name__ == "__main__":
    app = QApplication([])
    test_DownloadFile()
    test_InitiateFileInterationButtons()
    test_Request_Files()
    test_Send_login()
    test_UpdateFile()
    test_Delete_File()
    app.exec_()
