from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets, QtTest
import sys; sys.path += ['E://0//git//python-gachi-browser//code//resources//graphics']
from PanelHoldLabel import *
from PanelTab import *
from PushedLabel import *
from MenuLabel import *


class Ui_Main:
    
    def setupUi(self, Main):
        self.parent = Main
        self.label_panel = PanelHoldLabel(Main, Main.scene)
        self.label_panel.button_back = PushedLabel(Main, 'resources//images//left_arrow.png', 2, 31, 28, 20) 
        self.label_panel.button_forward = PushedLabel(Main, 'resources//images//right_arrow.png', 30, 31, 28, 20)
        self.label_panel.button_reload = PushedLabel(Main, 'resources//images//arrow_reload.png', 57, 30, 28, 20)
        self.label_panel.button_close = PushedLabel(Main, 'resources//images//cross.png', 1052, 4, 20, 20)
        self.label_panel.button_download = PushedLabel(Main, 'resources//images//button_download.png', 1048, 25, 28, 28)
        self.label_panel.button_scale = PushedLabel(Main, 'resources//images//button_scale.png', 1029, 4, 20, 20)
        self.label_panel.button_roll = PushedLabel(Main, 'resources//images//button_roll.png', 1006, 4, 20, 20)
        self.label_panel.button_menu = PushedLabel(Main, 'resources//images//button_menu.png', 978, 4, 20, 20)
        self.label_panel.button_menu.label_menu = MenuLabel(Main, 840, 26, 160)
        # self.label_panel.button_download.label_menu = MenuLabel(Main, 880, 55, 200, 600)
        # self.label_panel.addTab()
        # self.label_panel.addTab()
        # self.label_panel.addTab()
        # self.label_panel.addTab()
        # self.label_panel.addTab()
        # self.label_panel.addTab()

        self.connecting()

    def connecting(self):
        self.label_panel.button_reload.clicked.connect(self.reloadHandler)
        self.label_panel.button_back.clicked.connect(self.backHandler)
        self.label_panel.button_forward.clicked.connect(self.forwardHandler)
        self.label_panel.button_menu.clicked.connect(self.menuHandler)
        # self.label_panel.button_download.clicked.connect(self.downloadHandler)

    def reloadHandler(self):
        self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Reload).trigger()

    def backHandler(self):
        self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Back).trigger()

    def forwardHandler(self):
        self.label_panel.current_tab.scene.page.action(self.label_panel.current_tab.scene.page.Forward).trigger()

    def menuHandler(self):
        self.label_panel.button_menu.label_menu.setMenu()

    def downloadHandler(self):
        self.label_panel.button_download.label_menu.setMenu()