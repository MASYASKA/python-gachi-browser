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
        self.themes_title = QtWidgets.QLabel(self)
        font = self.history_title.font()
        self.history = HistoryWidget(self, 100, 65, 400, 400)
        self.themes = ThemesWidget(self)
        # calls
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.themes.setGeometry(self.width-140, 65, 80, self.themes.height)
        self.themes_title.setGeometry(self.width-140, 40, 80, 20)
        self.history_title.setGeometry(100, 20, 300, 35)
        self.history_title.setText("History")
        self.themes_title.setText("Themes")
        font.setPixelSize(36)
        self.history_title.setFont(font)
        font.setPixelSize(20)
        self.themes_title.setFont(font)

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
        self.themes_title.setGeometry(self.width-140, 40, 80, 20)
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
        self.scene.widget = BoxWidget()
        # calls
        self.scene.setSceneRect(0, 0, self.width-4, self.pos_y)
        self.scene.addWidget(self.scene.widget)
        self.scene.widget.setGeometry(0, 0, self.width-4, self.height)
        self.setScene(self.scene)
        self.setGeometry(self.x, self.y, self.width, self.height)

    def addUrl(self, title, url):
        print(title, url.toString()) # проблема в show()
        label = HistoryUrlLabel(self, self.scene.widget, 1, self.pos_y+1, self.width-4, 30)
        label.url = url
        label.title.setText(title)
        label.show()
        label.clicked.connect(self.historyTabHandler)
        self.label_lst += [label]
        self.pos_y += 30
        self.scene.setSceneRect(0, 0, self.width-4, self.pos_y)
        self.scene.widget.setGeometry(1, 1, self.width-4, self.pos_y)

    def historyTabHandler(self):
        url = self.sender().url
        # self.parent.parent.parent.parent.ui.label_panel.addTab(url)
        self.parent.parent.panel.addTab(url)



class BoxWidget(QtWidgets.QWidget):

    transformed = QtCore.pyqtSignal()

    def __init__(self):
        super(BoxWidget, self).__init__()


class ThemesWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(ThemesWidget, self).__init__(parent=parent)
        # params
        self.parent = parent
        self.x, self.y, self.width, self.height = self.parent.width-140, 65, 80, 0
        self.cx, self.cy, self.cwidth, self.cheight = 0, 0, 80, 20
        # items
        self.radio_greenTheme = QtWidgets.QRadioButton(self)
        self.radio_purpleTheme = QtWidgets.QRadioButton(self)
        self.radio_violetTheme = QtWidgets.QRadioButton(self)
        self.radio_cementTheme = QtWidgets.QRadioButton(self)
        # calls
        self.radio_greenTheme.setText('green')
        self.radio_purpleTheme.setText('purple')
        self.radio_violetTheme.setText('violet')
        self.radio_cementTheme.setText('cement')
        self.addRadio(self.radio_greenTheme)
        self.addRadio(self.radio_purpleTheme)
        self.addRadio(self.radio_violetTheme)
        self.addRadio(self.radio_cementTheme)

        self.connecting()

    def addRadio(self, radio):
        radio.setGeometry(self.cx, self.cy, self.cwidth, self.cheight)
        self.cy += self.cheight
        self.height = self.cy
        print(self.height)
        self.setGeometry(self.x, self.y, self.width, self.height)

    # themes

    def setGreenTheme(self):
        self.parent.parent.panel.setTheme(main="background-color: rgb(119, 221, 119);",
            tab_theme_selected="background-color : rgb(23, 114, 69);",
            tab_theme_unselected="background-color : background-color: rgb(119, 221, 119);",
            tab_theme_unselected_light="background-color : rgb(142, 230, 155);")

    def setPurpleTheme(self):
        self.parent.parent.panel.setTheme(main="background-color: rgb(152, 40, 158);",
            tab_theme_selected="background-color: rgb(255, 115, 0);", 
            tab_theme_unselected="background-color: rgb(152, 40, 158);",
            tab_theme_unselected_light="background-color: rgb(195, 49, 194);")

    def setVioletTheme(self):
        self.parent.parent.panel.setTheme(main="background-color: rgb(35, 0, 189);",
            tab_theme_selected="background-color: rgb(5, 165, 245);", 
            tab_theme_unselected="background-color: rgb(35, 0, 189);",
            tab_theme_unselected_light="background-color: rgb(59, 51, 181);")

    def setCementTheme(self):
        self.parent.parent.panel.setTheme(main='background-color: rgb(230, 230, 230);',
            tab_theme_selected='background-color: rgb(143, 143, 143);',
            tab_theme_unselected='background-color: rgb(230, 230, 230);',
            tab_theme_unselected_light='background-color: rgb(209, 209, 209);')

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.radio_greenTheme.clicked.connect(self.setGreenTheme)
        self.radio_purpleTheme.clicked.connect(self.setPurpleTheme)
        self.radio_violetTheme.clicked.connect(self.setVioletTheme)
        self.radio_cementTheme.clicked.connect(self.setCementTheme)

    def transform(self):
        self.setGeometry(self.parent.width-140, 65, 80, self.height)


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