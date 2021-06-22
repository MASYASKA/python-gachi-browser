from PyQt5 import QtWidgets, QtCore
from PushedLabel import *

class SettingsScene(QtWidgets.QGraphicsScene):

    transformed = QtCore.pyqtSignal()

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

        self.connecting()

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(self.x, self.y, self.width, self.height)
        self.transformed.emit()


class SceneMainWidget(QtWidgets.QWidget):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(SceneMainWidget, self).__init__()
        # params
        self.parent = parent
        self.x, self.y, self.width, self.height = 0, 0, parent.width, parent.height
        # items
        self.history_title = QtWidgets.QLabel(self)
        font = self.history_title.font()
        self.history = HistoryWidget(self, 100, 65, 400, 400)
        # calls
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.history_title.setGeometry(100, 25, 300, 30)
        self.history_title.setText("HISTORY")
        font.setPixelSize(36)
        self.history_title.setFont(font)

        self.connecting()

    def setTheme(self, main):
        for label in self.history.label_lst:
            label.setStyleSheet("QLabel{" + main.tab_theme_unselected + "}")
            label.tab_theme_unselected = main.tab_theme_unselected
            label.tab_theme_unselected_light = main.tab_theme_unselected_light

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        self.width, self.height = self.parent.width, self.parent.height
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.transformed.emit()


class HistoryWidget(QtWidgets.QGraphicsView):

    def __init__(self, parent, x, y, width, height):
        super(HistoryWidget, self).__init__(parent=parent)
        self.parent = parent
        self.x, self.y, self.width, self.height = x, y, width, height
        self.pos_y = 0
        self.label_lst = []
        # items
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.widget = MyWidget()
        # calls
        self.scene.setSceneRect(0, 0, self.width-4, self.pos_y)
        self.scene.addWidget(self.scene.widget)
        self.scene.widget.setGeometry(0, 0, self.width-4, self.height)
        self.setScene(self.scene)
        self.setGeometry(self.x, self.y, self.width, self.height)

    def addUrl(self, title, url):
        print(title, url.toString()) # проблема в show()
        label = HistoryUrlLabel(self, self.scene.widget, 0, self.pos_y, self.width-4, 30)
        label.url = url
        label.title.setText(title)
        label.show()
        label.clicked.connect(self.historyTabHandler)
        self.label_lst += [label]
        self.pos_y += 30
        self.scene.setSceneRect(0, 0, self.width-4, self.pos_y)
        self.scene.widget.setGeometry(0, 0, self.width-4, self.pos_y)

    def historyTabHandler(self):
        url = self.sender().url
        # self.parent.parent.parent.parent.ui.label_panel.addTab(url)
        self.parent.parent.panel.addTab(url)



class MyWidget(QtWidgets.QWidget):

    transformed = QtCore.pyqtSignal()

    def __init__(self):
        super(MyWidget, self).__init__()


class HistoryUrlLabel(PushedLabel):

    def __init__(self, parent, adoptive, x, y, width, height):
        super(HistoryUrlLabel, self).__init__(adoptive, '', x, y, width, height)
        # params
        self.parent = parent
        self.tab_theme_unselected = self.parent.parent.parent.panel.tab_theme_unselected
        self.tab_theme_unselected_light = self.parent.parent.parent.panel.tab_theme_unselected_light
        # items
        self.title = QtWidgets.QLabel(self)
        # calls
        self.title.setGeometry(10, 5, self.width-10-10, self.height-5-5)

    # events

    def enterEvent(self, event):
        self.setStyleSheet("QLabel{" + self.tab_theme_unselected_light + "}")

    def leaveEvent(self, event):
        self.setStyleSheet("QLabel{" + self.tab_theme_unselected + "}")