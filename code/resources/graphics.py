from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets, QtTest
from ui_class import Ui_Main as Ui_Main_old
from ui_class import *
from help_classes import *
import sys; sys.path += ['E://0//git//python-gachi-browser//code//resources']


class Ui_Main(Ui_Main_old):
    
    def setupUi(self, Main):
        self.parent = Main
        self.label_panel = PanelHoldLabel(Main, Main.scene)
        self.label_panel.edit_searchLine = SearchLineEdit(Main)
        self.label_panel.button_back = PushedLabel(Main, 'resources//images//left_arrow.png', 2, 31, 28, 20) 
        self.label_panel.button_forward = PushedLabel(Main, 'resources//images//right_arrow.png', 30, 31, 28, 20)
        self.label_panel.button_reload = PushedLabel(Main, 'resources//images//arrow_reload.png', 57, 30, 28, 20)
        self.label_panel.button_close = PushedLabel(Main, 'resources//images//cross.png', 1052, 4, 20, 20)
        self.label_panel.button_scale = PushedLabel(Main, 'resources//images//button_scale.png', 1029, 4, 20, 20)
        self.label_panel.button_roll = PushedLabel(Main, 'resources//images//button_roll.png', 1006, 4, 20, 20)

        # super(Ui_Main, self).setupUi(Main)
        self.connecting()

    def connecting(self):
        self.label_panel.button_back.clicked.connect(self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Back).trigger)
        self.label_panel.button_forward.clicked.connect(self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Forward).trigger)
        self.label_panel.button_reload.clicked.connect(self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Reload).trigger)