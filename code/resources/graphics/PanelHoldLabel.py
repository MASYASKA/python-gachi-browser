# structure
from PyQt5 import QtWidgets, QtCore
from MainPageView import *
from PushedLabel import *
from PanelTab import *
from PageScene import *

class PanelHoldLabel(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, scene):
        super(PanelHoldLabel, self).__init__(parent=parent)
        self.parent = parent
        self.scene = scene
        self.width, self.height = parent.width+10, 55
        self.setGeometry(-1, -1, self.width, self.height)
        self.setStyleSheet("QLabel{\n""    \n""    background-color: rgb(119, 221, 119);\n""}")
        self.view_current_page = ViewMainPage(parent)
        self.tab_count = 0
        self.tab_dict = dict([])
        self.tab_lst = []
        self.button_add_tab = PushedLabel(self, 'resources//images//button_add_tab.png', 0, 0, 25, 25)
        self.button_add_tab.clicked.connect(self.addTab)
        self.refresh()
        self.connecting()
        self.addTab()

    # tabs

    def addTab(self, url='https://www.google.com/'):
        tab = PanelTab(self, self.tab_count)
        scene = PageScene(self.view_current_page, url, tab)
        tab.scene = scene
        tab.show()
        self.tab_dict[f'tab_{self.tab_count}'] = tab
        self.tab_lst += [tab]
        self.tab_count += 1
        self.openTab(tab)
        self.refresh()

    def openTab(self, tab):
        self.view_current_page.setScene(tab.scene)
        self.current_tab = tab
        self.refresh()
        tab.raise_()

    def closeTab(self):
        tab = self.sender().parent
        for index in range(len(self.tab_lst)):
            if self.tab_lst[index] is tab:
                self.tab_lst.pop(index)
                break
        tab.delete()
        self.tab_count -= 1
        self.refresh()

    def moveTabForward(self, tab):
        try:
            index = self.tab_lst.index(tab)
            self.tab_lst[index], self.tab_lst[index+1] = self.tab_lst[index+1], self.tab_lst[index]
            self.tab_lst[index+1].x, self.tab_lst[index].x = self.tab_lst[index].x, self.tab_lst[index+1].x
            tab.press_event_coord_x = tab.move_event_coord_x
        except:
            pass

    def moveTabBack(self, tab):
        try:
            index = self.tab_lst.index(tab)
            self.tab_lst[index], self.tab_lst[index-1] = self.tab_lst[index-1], self.tab_lst[index]
            self.tab_lst[index].x, self.tab_lst[index-1].x = self.tab_lst[index-1].x, self.tab_lst[index].x
            tab.press_event_coord_x = tab.move_event_coord_x
        except:
            pass

    # helper functions

    def refresh(self):
        pos_x, pos_y = 0, 0
        for tab in self.tab_lst:
            if tab is self.current_tab:
                tab.setSelected()
            else:
                tab.setUnselected()
            tab.setGeometry(pos_x+2 , pos_y, tab.width, tab.height)
            pos_x += 140
        self.button_add_tab.setGeometry(pos_x, 0, 25, 25)
        self.button_add_tab.x = pos_x

    def setSceneSize(self):
        scene = self.current_tab.scene
        self.current_tab.setGeometry(0, 0, self.parent.width, self.parent.height)

    def load_current_page(self):
        url = QtCore.QUrl(f'https://www.google.com/search?q={self.edit_searchLine.text()}')
        self.current_tab.scene.engine.load(url)

    # events

    def mousePressEvent(self, event):
        self.mp = event.globalPos() - self.scene.view.pos()

    def mouseMoveEvent(self, event):
        try:
            self.scene.view.move(event.globalPos() - self.mp)
        except:
            pass

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('PanelHoldLabel here!')
        self.width = self.parent.width + 10 # self.height = const
        self.button_close.setGeometry(self.width-33, 4, 20, 20)
        self.button_scale.setGeometry(self.width-56, 4, 20, 20)
        self.button_roll.setGeometry(self.width-79, 4, 20, 20)
        self.button_menu.setGeometry(self.width-102, 4, 20, 20)
        self.button_menu.label_menu.setGeometry(self.width-272, 26, 190, 200)
        self.button_download.setGeometry(self.width-38, 25, 28, 28)
        self.edit_searchLine.setGeometry(94, 32, self.width-140, 18)
        self.setGeometry(0, 0, self.width, self.height)
        self.transformed.emit()