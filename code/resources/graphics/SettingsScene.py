from PyQt5 import QtWidgets, QtCore
from PushedLabel import *

class SettingsScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent, panel):
        super(SettingsScene, self).__init__()
        # params
        self.parent = parent
        self.panel = panel
        self.x, self.y, self.width, self.height = 0, 0, parent.width-2, parent.height-2
        # items
        self.widget = SceneMainWidget(self)
        # calls
        self.setSceneRect(self.x, self.y, self.width, self.height)
        self.addWidget(self.widget)


class SceneMainWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(SceneMainWidget, self).__init__()
        # params
        self.parent = parent
        self.x, self.y, self.width, self.height = 0, 0, parent.width, parent.height
        # items
        self.history = HistoryWidget(self, 250, 250, 200, 200)
        # calls
        self.setGeometry(self.x, self.y, self.width, self.height)


class HistoryWidget(QtWidgets.QWidget):

    def __init__(self, parent, x, y, width, height):
        super(HistoryWidget, self).__init__(parent=parent)
        self.parent = parent
        self.x, self.y, self.width, self.height = x, y, width, height
        self.pos_y = 0
        # items
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.widget = MyWidget()
        # calls
        self.scene.setSceneRect(0, 0, self.width-4, self.height)
        self.scene.addWidget(self.scene.widget)
        self.scene.widget.setGeometry(0, 0, self.width-4, self.height)
        # self.setScene(self.scene)
        self.setGeometry(self.x, self.y, self.width, self.height)

    def addUrl(self, title, url):
        print(title, url.toString())
        self.parent.button = QtWidgets.QPushButton(self.parent)


class MyWidget(QtWidgets.QWidget):

    transformed = QtCore.pyqtSignal()