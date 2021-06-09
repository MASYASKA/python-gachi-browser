from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets, QtTest

# structure


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
        self.button_add_tab = PushedLabel(self, 'resources//images//button_add_tab.png', 0, 0, 25, 25)
        self.button_add_tab.clicked.connect(self.addTab)
        self.refresh()
        self.connecting()
        self.addTab()

    # tabs

    def addTab(self, url='https://www.google.com/'):
        scene = PageScene(self.view_current_page, url)
        tab = PanelTab(self, scene, self.tab_count)
        tab.show()
        self.tab_dict[f'tab_{self.tab_count}'] = tab
        self.tab_count += 1
        self.openTab(tab)
        self.refresh()

    def openTab(self, tab):
        self.view_current_page.setScene(tab.scene)
        self.current_tab = tab

    def closeTab(self):
        tab = self.sender().parent
        tab.delete()
        self.tab_count -= 1
        self.refresh()

    # helper functions

    def mousePressEvent(self, event):
        self.mp = event.globalPos() - self.scene.view.pos()

    def mouseMoveEvent(self, event):
        try:
            self.scene.view.move(event.globalPos() - self.mp)
        except:
            pass

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('PanelHoldLabel here!')
        self.width = self.parent.width + 10 # self.height = const
        print(self.width, self.height)
        self.button_close.setGeometry(self.width-33, 4, 20, 20)
        self.button_scale.setGeometry(self.width-56, 4, 20, 20)
        self.button_roll.setGeometry(self.width-79, 4, 20, 20)
        self.edit_searchLine.setGeometry(94, 32, self.width-185, 18)
        self.button_sex.setGeometry(self.width-80, 31, 30, 20)
        self.button_searchCondition.setGeometry(self.width-42, 31, 30, 20)
        self.setGeometry(0, 0, self.width, self.height)
        self.transformed.emit()

    def refresh(self):
        pos_x, pos_y = 0, 0
        for key in self.tab_dict.keys():
            obj = self.tab_dict[key]
            obj.setGeometry(pos_x+2 , pos_y, obj.width, obj.height)
            pos_x += 95
        self.button_add_tab.setGeometry(pos_x, 0, 25, 25)
        self.button_add_tab.x = pos_x

    def setSceneSize(self):
        scene = self.current_tab.scene
        self.current_tab.setGeometry(0, 0, self.parent.width, self.parent.height)


class ViewMainPage(QtWidgets.QGraphicsView):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(ViewMainPage, self).__init__(parent=parent)
        self.parent = parent
        self.width, self.height = 1080, 666
        self.setGeometry(0, 54, self.width, self.height)
        self.connecting()

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('ViewMainPage here!')
        self.width, self.height = self.parent.width, self.parent.height-54
        self.setGeometry(0, 54, self.width, self.height)
        self.transformed.emit()


class PanelTab(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, scene, count):
        super(PanelTab, self).__init__(parent=parent)
        self.parent = parent
        self.id = f'tab_{count}'
        self.scene = scene
        if count > 0: self.x = 95*count
        else: self.x = 0
        self.y = 0
        self.width, self.height = 95, 25
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(r"QLabel{ background-color : white}")
        self.button_tab_close = PushedLabel(self, "resources//images//button_tab_close.png", 70, 0, 25, 25)
        self.button_tab_close.clicked.connect(self.parent.closeTab)
        self.connecting()

    def mousePressEvent(self, event):
        self.parent.openTab(self)

    def mouseMoveEvent(self, event):
        pass

    def delete(self):
        self.deleteLater()
        self.scene.deleteLater()
        self.scene.engine.deleteLater()
        del self.scene.engine
        del self.scene
        del self.parent.tab_dict[self.id]
        del self

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('PanelTab here!')
        self.transformed.emit()


class PageScene(QtWidgets.QGraphicsScene):

    changed = QtCore.pyqtSignal()
    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, url):
        super(PageScene, self).__init__()
        self.parent = parent
        self.width, self.height = parent.width-2, parent.height-2
        self.engine = ViewEnginePage(self)
        self.engine.load(QtCore.QUrl(url))
        self.page = self.engine.page()
        self.title = self.page.title()
        self.setSceneRect(0, 54, self.width, self.height)
        self.addWidget(self.engine)
        self.connecting()

    def action_page_back(self):
        self.changed.emit()

    def action_page_forward(self):
        self.changed.emit()

    def action_page_reload(self):
        self.changed.emit()

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('PageScene here!')
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(0, 54, self.width, self.height)
        self.transformed.emit()


class ViewEnginePage(QtWebEngineWidgets.QWebEngineView):

    def __init__(self, parent):
        super(ViewEnginePage, self).__init__()
        self.parent = parent
        self.width, self.height = parent.width, parent.height
        self.setGeometry(0, 54, self.width, self.height)
        self.connecting()

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('ViewMainPage here!')
        self.width, self.height = self.parent.width, self.parent.height
        self.setGeometry(0, 54, self.width, self.height)


# help classes

class PushedLabel(QtWidgets.QLabel, QtWidgets.QPushButton):

    clicked = QtCore.pyqtSignal()
    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, pixmap, x, y, width, height):
        super(PushedLabel, self).__init__(parent=parent)
        self.parent = parent
        self.x, self.y, self.width, self.height = x, y, width, height
        self.setPixmap(QtGui.QPixmap(pixmap))
        self.setGeometry(x, y, width, height)
        self.connecting()

    def mousePressEvent(self, event):
        # self.setGeometry(self.x+3, self.y+3, self.width-3, self.height-3)
        # QtTest.QTest.qWait(100)
        # self.setGeometry(self.x, self.y, self.width, self.height)
        self.clicked.emit()

    def mouseMoveEvent(self, event):
        pass

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('PushedLabel here!')
        self.transformed.emit()


class SearchLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent=parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.scene.button_sex_handler()
        else:
            super(SearchLineEdit, self).keyPressEvent(event)
