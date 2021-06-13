from PyQt5 import QtWidgets, QtCore
from PushedLabel import *

class MenuLabel(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, x, y, width, height):
        super(MenuLabel, self).__init__(parent=parent)
        self.parent = parent
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(r"QLabel{ background-color : white;}")
        self.setVisible(False)
        self.visible = False
        self.button_greenTheme = PushedLabel(self, 
            '', 0, 0, 160, 50)
        self.button_greenTheme.setStyleSheet("QLabel{ background-color : rgb(119, 221, 119); color: rgb(23, 114, 69);}")
        self.button_greenTheme.setText('GREEN')
        self.button_purpleTheme = PushedLabel(self,
            '', 0, 50, 160, 50)
        self.button_purpleTheme.setStyleSheet("QLabel{ background-color : rgb(152, 40, 158); color: rgb(255, 115, 0);}")
        self.button_purpleTheme.setText('PURPLE')

        self.cx, self.cy = 0, 0 # cx - children x
        self.cwidth, self.cheight = self.width, self.height/5
        self.connecting()

    def setMenu(self):
        if self.visible:
            self.setVisible(False)
            self.visible = False
        else:
            self.setVisible(True)
            self.visible = True

    def addButton(self, button):
        button.setGeometry(self.cx, self.cy, self.cwidth, self.cheight)
        button.setVisible(True)
        self.cy += self.cheight

    def connecting(self):
        self.button_greenTheme.clicked.connect(self.setGreenTheme)
        self.button_purpleTheme.clicked.connect(self.setPurpleTheme)


    def setGreenTheme(self):
        self.parent.ui.label_panel.setTheme(main="QLabel{background-color: rgb(119, 221, 119);}",
            tab_theme_selected="QLabel{ background-color : rgb(23, 114, 69);}",
            tab_theme_unselected="QLabel{ background-color : background-color: rgb(119, 221, 119);}",
            tab_theme_unselected_light="QLabel{ background-color : rgb(142, 230, 155)}")

    def setPurpleTheme(self):
        self.parent.ui.label_panel.setTheme(main="QLabel{background-color: rgb(152, 40, 158);}",
            tab_theme_selected="QLabel{background-color: rgb(255, 115, 0);}", 
            tab_theme_unselected="QLabel{background-color: rgb(152, 40, 158);}",
            tab_theme_unselected_light="QLabel{background-color: rgb(195, 49, 194);}")