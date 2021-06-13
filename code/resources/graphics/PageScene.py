from PyQt5 import QtWidgets, QtCore
from EnginePageView import *

class PageScene(QtWidgets.QGraphicsScene):

    changed = QtCore.pyqtSignal()
    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, url, tab):
        super(PageScene, self).__init__()
        self.parent = parent
        self.tab = tab
        self.width, self.height = parent.width-2, parent.height-2
        self.engine = ViewEnginePage(self)
        self.engine.load(QtCore.QUrl(url))
        self.page = self.engine.page()
        self.title = self.page.title()
        self.setSceneRect(0, 54, self.width, self.height)
        self.addWidget(self.engine)
        self.connecting()

    # helper functions

    def action_page_back(self):
        self.changed.emit()

    def action_page_forward(self):
        self.changed.emit()

    def action_page_reload(self):
        self.changed.emit()

    # required funcions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.engine.page().loadFinished.connect(self.tab.setPageName)

    def transform(self):
        print('PageScene here!')
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(0, 54, self.width, self.height)
        self.transformed.emit()