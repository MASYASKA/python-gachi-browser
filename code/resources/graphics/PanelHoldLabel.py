# structure
from PyQt5 import QtWidgets, QtCore
from MainPageView import *
from PushedLabel import *
from PanelTab import *
from PageScene import *
from SearchLineEdit import *
from StartPageScene import *

class PanelHoldLabel(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, scene):
        super(PanelHoldLabel, self).__init__(parent=parent)
        # params
        self.parent = parent
        self.scene = scene
        self.tab_count = 0
        self.tab_dict = dict([])
        self.tab_lst = []
        self.tab_stack = []
        self.is_start_page = False
        self.width, self.height = parent.width+10, 55
        self.panel_tab_width = self.width-112-25
        # style
        self.theme = "background-color: rgb(230, 230, 230);"
        self.tab_theme_selected = "background-color : rgb(143, 143, 143);"
        self.tab_theme_unselected = "background-color: rgb(230, 230, 230);"
        self.tab_theme_unselected_light = "background-color : rgb(209, 209, 209);"
        # items
        self.view_current_page = ViewMainPage(parent)
        self.start_page = StartPageScene(self.view_current_page, self)
        self.button_setStartPage = PushedLabel(self, 'resources//images//button_open_start_page.png', 0, 0, 25, 25)
        self.edit_searchLine = SearchLine(self)
        # calls
        self.setGeometry(-1, -1, self.width, self.height)
        self.setStyleSheet("QLabel{" + self.theme + "}")
        self.refresh()
        self.setTheme(self.theme, self.tab_theme_selected, self.tab_theme_unselected, self.tab_theme_unselected_light)
        # self.addTab() # нельзя добавлять таб изначально, потому что панель не инициализирована
        self.connecting()

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
        print(self)
        try:
            index = self.tab_stack.index(tab)
            del self.tab_stack[index]
            self.tab_stack += [tab]
        except ValueError:
            self.tab_stack += [tab]
        # self.refresh() # multiplie calls when adding tab
        self.edit_searchLine.line_edit.setEditTitle()
        self.edit_searchLine.line_edit_title.setVisible(True)
        self.edit_searchLine.line_edit.setText('')
        self.edit_searchLine.line_edit.setPlaceholderText("")
        # self.closeStartPage() # !!!!!!!!!!!! recursion on openTab
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
        self.tab_stack.pop(self.tab_stack.index(tab))
        try:
            self.openTab(self.tab_stack[-1]) # if it is last tab
        except:
            self.setStartPage()
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

    # start page

    def setStartPage(self):
        if self.is_start_page:
            self.closeStartPage()
        else:
            self.openStartPage()

    def openStartPage(self):
        self.view_current_page.setScene(self.start_page)
        self.button_setStartPage.setPixmap(QtGui.QPixmap('resources//images//button_close_start_page.png'))
        self.button_setStartPage.setStyleSheet("QLabel{background-color:" + self.tab_theme_unselected_light +"}")
        self.is_start_page = True
        self.current_tab = None # для того чтобы последний выбранный таб не подсвечивался
        self.edit_searchLine.line_edit.setText("")
        self.edit_searchLine.line_edit_title.setText("")
        self.refresh()

    def closeStartPage(self):
        self.button_setStartPage.setPixmap(QtGui.QPixmap('resources//images//button_open_start_page.png'))
        self.button_setStartPage.setStyleSheet("QLabel{}")
        self.is_start_page = False
        try:
            self.openTab(self.tab_stack[-1])
        except:
            # self.parent.parent.parent.close()
            pass

    # helper functions

    def refresh(self):
        pos_x, pos_y = 0, 0
        suma = 0
        width = 140
        for tab in self.tab_lst:
            suma += tab.width
        if suma >= self.panel_tab_width:
            width = self.panel_tab_width / len(self.tab_lst)
            # print(width)
        # if sum([tab.width for tab in self.tab_lst]) >= self.panel_tab_width:
        #     width = self.panel_tab_width / tab.width
        #     print(width)
        for tab in self.tab_lst:
            # tab.width = width
            if tab is self.current_tab:
                tab.setSelected()
            else:
                tab.setUnselected()
            tab.setGeometry(pos_x+2 , pos_y, tab.width, tab.height)
            pos_x += width
        print(pos_x)
        self.button_setStartPage.setGeometry(pos_x, 0, 25, 25)
        self.button_setStartPage.x = pos_x

    def setSceneSize(self):
        scene = self.current_tab.scene
        self.current_tab.setGeometry(0, 0, self.parent.width, self.parent.height)

    def load_current_page(self, turn):
        if turn:
            url = QtCore.QUrl(self.edit_searchLine.line_edit.text())
        else:
            url = QtCore.QUrl(f'https://www.google.com/search?q={self.edit_searchLine.line_edit.text()}')
        try:
            try:
                self.current_tab.scene.engine.load(url)
            except AttributeError:
                self.addTab()
                self.current_tab.scene.engine.load(url)
        except RuntimeError:
            self.addTab()
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
        self.button_setStartPage.clicked.connect(self.setStartPage)

    def transform(self):
        print('PanelHoldLabel here!')
        self.width = self.parent.width + 10 # self.height = const
        self.button_close.setGeometry(self.width-33, 4, 20, 20)
        self.button_scale.setGeometry(self.width-56, 4, 20, 20)
        self.button_roll.setGeometry(self.width-79, 4, 20, 20)
        self.button_menu.setGeometry(self.width-102, 4, 20, 20)
        self.button_menu.label_menu.setGeometry(self.width-245, self.button_menu.label_menu.y, 
                        self.button_menu.label_menu.width, self.button_menu.label_menu.height)
        # self.button_download.label_menu.setGeometry(self.width-210, 55, 200, 600)
        self.button_download.setGeometry(self.width-38, 25, 28, 28)
        self.edit_searchLine.setGeometry(94, 32, self.width-140, 18)
        self.edit_searchLine.x, self.edit_searchLine.y, self.edit_searchLine.width, self.edit_searchLine.height = 94, 32, self.width-140, 18
        self.setGeometry(0, 0, self.width, self.height)
        self.tab_width = self.width-112
        self.transformed.emit()

    def setTheme(self, main, tab_theme_selected, tab_theme_unselected, tab_theme_unselected_light):
        self.setStyleSheet("QLabel{" + main + "}")
        self.tab_theme_selected = tab_theme_selected
        self.tab_theme_unselected = tab_theme_unselected
        self.tab_theme_unselected_light = tab_theme_unselected_light
        self.edit_searchLine.line_edit.setTheme(self)
        self.start_page.widget.setTheme(self)
        self.refresh()