from PyQt5 import QtWidgets, QtCore
from EnginePageView import *

class PageScene(QtWidgets.QGraphicsScene):

    changed = QtCore.pyqtSignal()
    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, url, tab):
        super(PageScene, self).__init__()
        # params
        self.parent = parent
        self.tab = tab
        self.width, self.height = parent.width-2, parent.height-2
        # items
        self.engine = ViewEnginePage(self)
        self.page = self.engine.page()
        # calls
        self.engine.load(QtCore.QUrl(url))
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

    def addUrlToHistory(self):
        self.parent.parent.ui.label_panel.settings_page.widget.history.addUrl(self.engine.page().title(), self.engine.page().url())


    # required funcions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.engine.page().loadFinished.connect(self.tab.setPageName)
        self.engine.page().loadFinished.connect(self.parent.parent.ui.label_panel.edit_searchLine.line_edit.setEditTitle)
        self.engine.page().loadFinished.connect(self.addUrlToHistory)

    def transform(self):
        print('PageScene here!')
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(0, 54, self.width, self.height)
        self.transformed.emit()