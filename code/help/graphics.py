from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
from ui_class import Ui_Main as Ui_Main_old
from ui_class import *


class Ui_Main(Ui_Main_old):
    
    def setupUi(self, Main):
        self.label_panel = PanelHoldButton(Main, Main.scene)
        super(Ui_Main, self).setupUi(Main)
        self.button_searchCondition.setText('🔍')
        font = QtGui.QFont()
        font.setPointSize(5)
        self.button_searchCondition.setFont(font)
        self.button_searchCondition.clicked.connect(self.changeCondition)
        self.button_searchCondition.search_site = False
        self.edit_searchLine = SearchLineEdit(Main)
        self.edit_searchLine.setGeometry(QtCore.QRect(94, 32, 900, 18))
        self.edit_searchLine.setObjectName("edit_searchLine")

    def changeCondition(self):
        if self.button_searchCondition.search_site:
            self.button_searchCondition.search_site = False
            self.button_searchCondition.setText('🔍')
        else:
            self.button_searchCondition.search_site = True
            self.button_searchCondition.setText('🌏')

    def setUiSize(self, width, height):
        self.edit_searchLine.setGeometry(94, 32, width-200, 18)
        self.button_sex.setGeometry(width-80, 31, 30, 20)
        self.button_searchCondition.setGeometry(width-38, 31, 30, 20)
        self.button_close.setGeometry(width-30, 4, 18, 18)
        self.button_scale.setGeometry(width-53, 4, 18, 18)
        self.button_roll.setGeometry(width-76, 4, 18, 18)

class SearchLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent=parent)
        self.widget = parent

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.widget.scene.button_sex_handler()
        else:
            super(SearchLineEdit, self).keyPressEvent(event)

class PanelHoldButton(QtWidgets.QLabel):

    def __init__(self, parent, scene):
        super(PanelHoldButton, self).__init__(parent=parent)
        self.scene = scene
        self.setGeometry(-1, -1, 1090, 55)
        self.setStyleSheet("QLabel{\n"
"    \n"
"    background-color: rgb(167, 229, 255);\n"
"}")

    def mousePressEvent(self, event):
        self.mp = event.globalPos() - self.scene.view.pos()

    def mouseMoveEvent(self, event):
        self.scene.view.move(event.globalPos() - self.mp)


class MyEngineView(QtWebEngineWidgets.QWebEngineView):

    def __init__(self):
        super(MyEngineView, self).__init__()
        self.setGeometry(0, 54, 1080, 666)
        self.load(QtCore.QUrl('https://www.google.com/'))