from PyQt5 import QtWidgets, QtCore
from PushedLabel import *
import settings_parser
import os
import sys
settings = settings_parser.Parser('E://0//git//python-gachi-browser//code//settings.txt')

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
        self.performance_title = QtWidgets.QLabel(self)
        font = self.history_title.font()
        self.history = HistoryWidget(self, 100, 65, 400, 400)
        self.themes = ThemesWidget(self)
        self.performance = PerformanceWidget(self)
        # calls
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.themes.setGeometry(self.width-140, 65, 80, self.themes.height)
        self.themes_title.setGeometry(self.width-140, 40, 80, 20)
        self.history_title.setGeometry(100, 20, 300, 35)
        self.performance_title.setGeometry(self.parent.width-400, 45, 114, 20)
        self.history_title.setText("History")
        self.themes_title.setText("Themes")
        self.performance_title.setText("Performance")
        font.setPixelSize(36)
        self.history_title.setFont(font)
        font.setPixelSize(20)
        self.themes_title.setFont(font)
        self.performance_title.setFont(font)

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
        self.performance_title.setGeometry(self.parent.width-400, 45, 114, 20)
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

class RadioWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RadioWidget, self).__init__(parent=parent)
        # params
        self.parent = parent
        self.x, self.y, self.width, self.height = 0, 0, 0, 0
        self.cx, self.cy, self.cwidth, self.cheight = 0, 0, 0, 0

    def addRadio(self, radio):
        radio.setGeometry(self.cx, self.cy, self.cwidth, self.cheight)
        self.cy += self.cheight
        self.height = self.cy
        self.setGeometry(self.x, self.y, self.width, self.height)


class PerformanceWidget(RadioWidget):

    def __init__(self, parent):
        super(PerformanceWidget, self).__init__(parent=parent)
        # params
        self.x, self.y, self.width, self.height = self.parent.width-400, 65, 80, 0
        self.cx, self.cy, self.cwidth, self.cheight = 0, 0, 80, 20
        # items
        self.radio_boostOn = QtWidgets.QRadioButton(self)
        self.radio_boostOff = QtWidgets.QRadioButton(self)
        self.message = QtWidgets.QMessageBox()
        # calls
        self.radio_boostOn.setText('performance')
        self.radio_boostOff.setText('functionality')
        self.addRadio(self.radio_boostOn)
        self.addRadio(self.radio_boostOff)
        self.message.setText('Browser will restart')
        self.message.setInformativeText('Continue?')
        self.message.addButton(QtWidgets.QWidget().tr('Yes'), self.message.AcceptRole)
        self.message.addButton(QtWidgets.QWidget().tr('No'), self.message.RejectRole)
        if settings.optimized == 'True':
            self.radio_boostOn.setChecked(True)
        else:
            self.radio_boostOff.setChecked(True)

        self.connecting()

    def boost_on(self):
        settings.dic['optimized'] = 'True'
        settings.fill()
        self.message.exec()

    def boost_off(self):
        settings.dic['optimized'] = 'False'
        settings.fill()
        self.message.exec()

    # restart

    def restart_browser(self):
        os.execv(sys.executable, [sys.executable] + sys.argv)

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.radio_boostOn.clicked.connect(self.boost_on)
        self.radio_boostOff.clicked.connect(self.boost_off)
        self.message.accepted.connect(self.restart_browser)

    def transform(self):
        self.setGeometry(self.parent.width-400, 65, 80, self.height)


class ThemesWidget(RadioWidget):

    def __init__(self, parent):
        super(ThemesWidget, self).__init__(parent=parent)
        # params
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
        self.radio_cementTheme.setChecked(True)

        self.connecting()

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