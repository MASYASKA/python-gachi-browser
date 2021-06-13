from PyQt5 import QtWidgets, QtCore, QtGui

class PushedLabel(QtWidgets.QLabel, QtWidgets.QPushButton):

    clicked = QtCore.pyqtSignal()
    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, pixmap, x, y, width, height):
        super(PushedLabel, self).__init__(parent=parent)
        self.parent = parent
        self.x, self.y, self.width, self.height = x, y, width, height
        self.setPixmap(QtGui.QPixmap(pixmap))
        self.setGeometry(x, y, width, height)
        self.connecting()

    # events

    def mousePressEvent(self, event):
        # self.setGeometry(self.x+3, self.y+3, self.width-3, self.height-3)
        # QtTest.QTest.qWait(100)
        # self.setGeometry(self.x, self.y, self.width, self.height)
        self.clicked.emit()

    def mouseMoveEvent(self, event):
        pass

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('PushedLabel here!')
        self.transformed.emit()