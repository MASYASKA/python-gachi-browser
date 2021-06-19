from PyQt5 import QtWidgets, QtCore
from PushedLabel import *


class StartPageScene(QtWidgets.QGraphicsScene):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(StartPageScene, self).__init__()
        self.parent = parent
        self.x, self.y, self.width, self.height = 0, 0, parent.width-2, parent.height-2
        self.setSceneRect(self.x, self.y, self.width, self.height)
        self.widget_layout = QtWidgets.QWidget()
        self.widget_layout.setGeometry(80, 25, self.width-80-80, 260)
        self.widget_layout.layout = QtWidgets.QGridLayout()
        self.widget_layout.layout.setVerticalSpacing(20)
        self.widget_layout.layout.setHorizontalSpacing(20)
        self.widget_layout.setLayout(self.widget_layout.layout)
        self.addWidget(self.widget_layout)
        self.line, self.column = 0, 0
        self.addBookmark('https://znanija.com/')
        self.addBookmark('https://www.youtube.com/')
        self.addBookmark('https://www.google.com/')
        self.addBookmark('e э э')
        self.addBookmark('e э э')
        self.addBookmark('e э э')
        self.addBookmark('e э э')
        self.addBookmark('e э э')


        self.connecting()

    # 

    def addBookmark(self, url):
        bookmark = BookmarkLabel(self, url)
        self.widget_layout.layout.addWidget(bookmark, self.line, self.column)
        if self.column > 4:
            self.column = 0
            self.line += 1
        else:
            self.column += 1

    def setTheme(self):
        self.widget_layout.setStyleSheet("QWidget{" + self.parent.parent.ui.label_panel.tab_theme_unselected_light
                                            + "}")

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(self.x, self.y, self.width, self.height)
        self.widget_layout.setGeometry(80, 25, self.width-80-80, 260)


class BookmarkLabel(QtWidgets.QLabel):

    def __init__(self, parent, url):
        super(BookmarkLabel, self).__init__()
        self.parent = parent
        self.url = url
        self.setText(self.url)
        self.setStyleSheet("QLabel{background-color: yellow; border-radius: 5px;}")
        self.setGeometry(250, 250, 100, 100)

    def mousePressEvent(self, event):
        self.parent.parent.parent.ui.label_panel.addTab(self.url)