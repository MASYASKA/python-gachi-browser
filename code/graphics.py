from PyQt5 import QtWidgets, QtGui, QtCore
from ui_class import *
from ui_class import Ui_Main as Ui_Main_old


class Ui_Main(Ui_Main_old):
    pass

class PanelHoldButton(QtWidgets.QPushButton):

    def __init__(self, parent, scene):
        super(PanelHoldButton, self).__init__(parent=parent)
        self.scene = scene
        self.setGeometry(-1, -1, 1090, 30)
        self.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: rgb(167, 229, 255);\n"
"}")

    def mousePressEvent(self, event):
        self.mp = event.globalPos() - self.scene.view.pos()

    def mouseMoveEvent(self, event):
        self.scene.view.move(event.globalPos() - self.mp)