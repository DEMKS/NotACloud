"""
This is not a App
"""
import sys
from PySide2 import QtWidgets


class Test(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('TestApp')
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = Test()
    sys.exit(app.exec_())
