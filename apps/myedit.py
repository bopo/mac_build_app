from PyQt5.Qt import *


class FileEdit(QLineEdit):

    def __init__(self, *args, **kwargs):
        super(FileEdit, self).__init__(*args)
        self.setAcceptDrops(True)  # 设置接受拖放动作
        self.setToolTip(self.text())
        self.setClearButtonEnabled(1)
        self.textChanged.connect(lambda: self.setToolTip(self.text()))
        self.textChanged.connect(self.repaint)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        path = e.mimeData().text().replace('file://', '')
        if path[-1] == '/':
            path = path[:-1]
        self.setText(path)


class FolderEdit(FileEdit):
    pass
