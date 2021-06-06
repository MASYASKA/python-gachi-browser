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


class PanelHoldButton(QtWidgets.QLabel):

    def __init__(self, parent, scene):
        super(PanelHoldButton, self).__init__(parent=parent)
        self.scene = scene
        self.setGeometry(-1, -1, 1090, 55)
        self.setStyleSheet("QLabel{\n"
"    \n"
"    background-color: rgb(167, 229, 255);\n"
"}")
        self.view_current_page = ViewMainPage(parent)
        self.tab_count = 0

    def addTab(self, url='https://www.google.com/'):
        scene = PageScene(self.view_current_page, url)
        tab = PanelTab(self, scene)
        tab.id = f'tab_{self.tab_count}'
        self.__dict__[tab.id] = tab
        self.tab_count += 1
        self.openTab(tab.id)
        self.current_tab = tab

    def openTab(self, tab_id):
        self.view_current_page.setScene(self.__dict__[tab_id].scene)

    # helper functions

    def mousePressEvent(self, event):
        self.mp = event.globalPos() - self.scene.view.pos()

    def mouseMoveEvent(self, event):
        self.scene.view.move(event.globalPos() - self.mp)


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
        self.x, self.y, self.width, self.height = x, y, width, height
        self.setPixmap(QtGui.QPixmap(pixmap))
        self.setGeometry(x, y, width, height)

    def mousePressEvent(self, event):
        self.clicked.emit()
        self.setGeometry(self.x+3, self.y+3, self.width-3, self.height-3)
        QtTest.QTest.qWait(100)
        self.setGeometry(self.x, self.y, self.width, self.height)


class PanelTab(QtWidgets.QLabel):

    def __init__(self, parent, scene):
        super(PanelTab, self).__init__(parent=parent)
        self.scene = scene
        self.setGeometry(0, 0, 95, 25)
        self.setStyleSheet(r"QLabel{ background-color : black}")


class ViewMainPage(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(ViewMainPage, self).__init__(parent=parent)
        self.width, self.height = 1080, 666
        self.setGeometry(0, 54, self.width, self.height)