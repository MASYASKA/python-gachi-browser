from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets, QtTest


class SearchLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent=parent)
        self.widget = parent

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.widget.scene.button_sex_handler()
        else:
            super(SearchLineEdit, self).keyPressEvent(event)


class PanelHoldLabel(QtWidgets.QLabel):

    def __init__(self, parent, scene):
        super(PanelHoldLabel, self).__init__(parent=parent)
        self.scene = scene
        self.setGeometry(-1, -1, 1090, 55)
        self.setStyleSheet("QLabel{\n"
"    \n"
"    background-color: rgb(167, 229, 255);\n"
"}")
        self.view_current_page = ViewMainPage(parent)
        self.tab_count = 0
        self.tab_dict = dict([])

    def addTab(self, url='https://www.google.com/'):
        scene = PageScene(self.view_current_page, url)
        # self.__dict__[f'tab_{self.tab_count}'] = 'loading...'
        tab = PanelTab(self, scene, self.tab_count)
        self.tab_dict[f'tab_{self.tab_count}'] = tab
        # self.__dict__[tab.id] = tab
        self.tab_count += 1
        self.openTab(tab)

    def openTab(self, tab):
        self.view_current_page.setScene(tab.scene)
        self.current_tab = tab

    def closeTab(self):
        tab = self.sender().parent
        tab.delete()
        self.tab_count -= 1
        self.refresh()

    def refresh(self):
        pos_x, pos_y = 0, 0
        for key in self.tab_dict.keys():
            obj = self.tab_dict[key]
            obj.setGeometry(pos_x, pos_y, obj.width, obj.height)
            pos_x += 96

    # helper functions

    def mousePressEvent(self, event):
        self.mp = event.globalPos() - self.scene.view.pos()

    def mouseMoveEvent(self, event):
        try:
            self.scene.view.move(event.globalPos() - self.mp)
        except:
            pass


class PageScene(QtWidgets.QGraphicsScene):

    changed = QtCore.pyqtSignal()

    def __init__(self, parent, url):
        super(PageScene, self).__init__()
        self.width, self.height = parent.width-2, parent.height-2
        self.engine = ViewEnginePage(self)
        self.engine.load(QtCore.QUrl(url))
        self.page = self.engine.page()
        self.title = self.page.title()
        self.setSceneRect(0, 54, self.width, self.height)
        self.addWidget(self.engine)

    def action_page_back(self):
        self.changed.emit()

    def action_page_forward(self):
        self.changed.emit()

    def action_page_reload(self):
        self.changed.emit()


class ViewEnginePage(QtWebEngineWidgets.QWebEngineView):

    def __init__(self, parent):
        super(ViewEnginePage, self).__init__()
        self.setGeometry(0, 54, parent.width, parent.height)


class PushedLabel(QtWidgets.QLabel, QtWidgets.QPushButton):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent, pixmap, x, y, width, height):
        super(PushedLabel, self).__init__(parent=parent)
        self.parent = parent
        self.x, self.y, self.width, self.height = x, y, width, height
        self.setPixmap(QtGui.QPixmap(pixmap))
        self.setGeometry(x, y, width, height)

    def mousePressEvent(self, event):
        self.setGeometry(self.x+3, self.y+3, self.width-3, self.height-3)
        QtTest.QTest.qWait(100)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.clicked.emit()


class PanelTab(QtWidgets.QLabel):

    def __init__(self, parent, scene, count):
        super(PanelTab, self).__init__(parent=parent)
        self.id = f'tab_{count}'
        self.scene = scene
        self.parent = parent
        if count > 0: self.x = 95*count + 1
        else: self.x = 0
        self.y = 0
        self.width, self.height = 95, 25
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(r"QLabel{ background-color : white}")
        self.button_close = PushedLabel(self, "resources//images//button_tab_close.png", 70, 0, 25, 25)
        self.button_close.clicked.connect(self.parent.closeTab)


    def mousePressEvent(self, event):
        self.parent.openTab(self)

    def delete(self):
        self.deleteLater()
        self.scene.deleteLater()
        self.scene.engine.deleteLater()
        del self.scene.engine
        del self.scene
        del self.parent.tab_dict[self.id]
        del self



class ViewMainPage(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(ViewMainPage, self).__init__(parent=parent)
        self.width, self.height = 1080, 666
        self.setGeometry(0, 54, self.width, self.height)