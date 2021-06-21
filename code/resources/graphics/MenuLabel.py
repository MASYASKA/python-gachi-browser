from PyQt5 import QtWidgets, QtCore
from PushedLabel import *

class MenuLabel(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, x, y, width, height=0):
        super(MenuLabel, self).__init__(parent=parent)
        # params
        self.parent = parent
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.cx, self.cy = 0, 0 # cx - children x
        self.cwidth, self.cheight = self.width, 20
        self.visible = False
        # items
        self.button_greenTheme = PopupMenuLabel(self, 'green theme')
        self.button_purpleTheme = PopupMenuLabel(self, 'purple theme')
        self.button_violetTheme = PopupMenuLabel(self, 'violet theme')
        self.button_cementTheme = PopupMenuLabel(self, 'cement theme')
        # calls
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(r"QLabel{ background-color : white;}")
        self.setVisible(False)
        self.addButton(self.button_greenTheme)
        self.addButton(self.button_purpleTheme)
        self.addButton(self.button_violetTheme)
        self.addButton(self.button_cementTheme)

        self.connecting()

    def setMenu(self):
        if self.visible:
            self.setVisible(False)
            self.visible = False
            self.setFocus(False)
        else:
            self.setVisible(True)
            self.visible = True
            self.setFocus(True)

    def addButton(self, button):
        button.setGeometry(self.cx, self.cy, self.cwidth, self.cheight)
        button.label_text.setGeometry(15, 2, self.cwidth-25, self.cheight-5)
        self.cy += self.cheight
        self.height += self.cheight
        self.setGeometry(self.x, self.y, self.width, self.height)


    def setGreenTheme(self):
        self.parent.ui.label_panel.setTheme(main="background-color: rgb(119, 221, 119);",
            tab_theme_selected="background-color : rgb(23, 114, 69);",
            tab_theme_unselected="background-color : background-color: rgb(119, 221, 119);",
            tab_theme_unselected_light="background-color : rgb(142, 230, 155);")

    def setPurpleTheme(self):
        self.parent.ui.label_panel.setTheme(main="background-color: rgb(152, 40, 158);",
            tab_theme_selected="background-color: rgb(255, 115, 0);", 
            tab_theme_unselected="background-color: rgb(152, 40, 158);",
            tab_theme_unselected_light="background-color: rgb(195, 49, 194);")

    def setVioletTheme(self):
        self.parent.ui.label_panel.setTheme(main="background-color: rgb(35, 0, 189);",
            tab_theme_selected="background-color: rgb(5, 165, 245);", 
            tab_theme_unselected="background-color: rgb(35, 0, 189);",
            tab_theme_unselected_light="background-color: rgb(59, 51, 181);")

    def setCementTheme(self):
        self.parent.ui.label_panel.setTheme(main='background-color: rgb(230, 230, 230);',
            tab_theme_selected='background-color: rgb(143, 143, 143);',
            tab_theme_unselected='background-color: rgb(230, 230, 230);',
            tab_theme_unselected_light='background-color: rgb(209, 209, 209);')

    # events

    def focusOutEvent(self, event):
        self.visible = False
        self.setVisible(self.visible)

    # required functions

    def connecting(self):
        self.button_greenTheme.clicked.connect(self.setGreenTheme)
        self.button_purpleTheme.clicked.connect(self.setPurpleTheme)
        self.button_violetTheme.clicked.connect(self.setVioletTheme)
        self.button_cementTheme.clicked.connect(self.setCementTheme)



class PopupMenuLabel(PushedLabel):

    def __init__(self, parent, text, x=1, y=1, width=1, height=1):
        super(PopupMenuLabel, self).__init__(parent=parent, pixmap='', x=x, y=y, width=width, height=height)
        self.setStyleSheet("QLabel{background-color: white;}")
        self.label_text = QtWidgets.QLabel(self)
        self.label_text.setGeometry(15, 5, self.width-25, self.height-5)
        self.label_text.setText(text)

    # events

    def enterEvent(self, event):
        self.setStyleSheet("QLabel{background-color: rgb(163, 163, 163);}")

    def leaveEvent(self, event):
        self.setStyleSheet("QLabel{background-color: white;}")