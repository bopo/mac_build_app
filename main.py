# coding=utf-8
from apps.tools import *
from apps.app import MainWin


if __name__ == '__main__':
    app = QApplication([])
    win = MainWin()
    win.show()
    app.exec_()