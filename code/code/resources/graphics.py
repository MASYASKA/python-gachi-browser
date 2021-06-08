from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets, QtTest
from ui_class import Ui_Main as Ui_Main_old
from ui_class import *
from help_classes import *
import sys; sys.path += ['E://0//git//python-gachi-browser//code//code//resources']


class Ui_Main(Ui_Main_old):
    
    def setupUi(self, Main):
        self.label_panel = PanelHoldLabel(Main, Main.scene)
        self.button_back = PushedLabel(Main, 'resources//images//left_arrow.png', 2, 31, 28, 20) 
        self.button_forward = PushedLabel(Main, 'resources//images//right_arrow.png', 30, 31, 28, 20)
        self.button_reload = PushedLabel(Main, 'resources//images//arrow_reload.png', 57, 30, 28, 20)
        self.button_close = PushedLabel(Main, 'resources//images//cross.png', 1052, 4, 20, 20)
        self.button_scale = PushedLabel(Main, 'resources//images//button_scale.png', 1029, 4, 20, 20)
        self.button_roll = PushedLabel(Main, 'resources//images//button_roll.png', 1006, 4, 20, 20)
        self.label_panel.view_current_page = ViewMainPage(Main)
        self.label_panel.addTab()

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
        self.connecting()

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
        self.button_close.setGeometry(width-30, 4, 20, 20)
        self.button_scale.setGeometry(width-53, 4, 20, 20)
        self.button_roll.setGeometry(width-76, 4, 20, 20)
        self.label_panel.setGeometry(0, 0, width+10, 55)
        self.label_panel.view_current_page.setGeometry(0, 54, width, height-55)


    def connecting(self):
        self.button_back.clicked.connect(self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Back).trigger)
        self.button_forward.clicked.connect(self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Forward).trigger)
        self.button_reload.clicked.connect(self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Reload).trigger)