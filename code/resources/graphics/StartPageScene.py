from PyQt5 import QtWidgets, QtCore
from PushedLabel import *


class StartPageScene(QtWidgets.QGraphicsScene):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(StartPageScene, self).__init__()
        self.parent = parent
        self.x, self.y, self.width, self.height = 0, 0,  parent.width-2, parent.height-2
        
        self.widget = SceneMainWidget(self)

        self.setSceneRect(self.x, self.y, self.width, self.height)
        self.addWidget(self.widget)

        self.connecting()

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(self.x, self.y, self.width, self.height)
        self.transformed.emit()


class SceneMainWidget(QtWidgets.QWidget):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(SceneMainWidget, self).__init__()
        self.parent = parent
        self.x, self.y, self.width, self.height = 0, 0, parent.width, parent.height
        self.line, self.column = 0, 0
        self.bookmark_lst = []

        self.button_addBookmark = PushedLabel(self, 'button_add_bookmark.png', self.width-80-25, 310, 25, 25)
        self.widget_layout = QtWidgets.QWidget(self)
        self.widget_layout.layout = QtWidgets.QGridLayout()

        self.widget_layout.setGeometry(80, 25, self.width-80-80, 260)
        self.widget_layout.layout.setVerticalSpacing(40)
        self.widget_layout.layout.setHorizontalSpacing(40)
        self.widget_layout.setLayout(self.widget_layout.layout)
        self.setGeometry(0, 0, self.width, self.height)
        self.addBookmark('https://znanija.com/')
        self.addBookmark('https://www.youtube.com/')
        self.addBookmark('https://www.google.com/')
        self.addBookmark('https://stackoverflow.com/')
        self.addBookmark('https://github.com/')
        self.addBookmark('https://pypi.org/')
        self.addBookmark('https://znanija.com/')
        self.addBookmark('https://www.youtube.com/')
        self.addBookmark('https://www.google.com/')
        self.addBookmark('https://stackoverflow.com/')
        self.addBookmark('https://github.com/')
        self.addBookmark('ПАШОЛ НАХУЙ')

        self.connecting()

    # 

    def addBookmark(self, url):
        bookmark = BookmarkLabel(self, url)
        bookmark.setStyleSheet("QLabel{background-color:black;}")
        self.widget_layout.layout.addWidget(bookmark, self.line, self.column)
        self.bookmark_lst += [bookmark]
        if self.column > 4:
            self.column = 0
            self.line += 1
        else:
            self.column += 1

    def setTheme(self, main):
        self.widget_layout.setStyleSheet("QWidget{" + main.tab_theme_unselected
                                            + "}")
        for qbookmark in self.bookmark_lst:
            qbookmark.setStyleSheet("Qlabel{" + main.tab_theme_selected + "border-radius: 5px;}")
            qbookmark.tab_theme_unselected = main.tab_theme_unselected
            qbookmark.tab_theme_unselected_light = main.tab_theme_unselected_light

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        self.width, self.height = self.parent.width, self.parent.height
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.widget_layout.setGeometry(80, 25, self.width-80-80, 260)


class BookmarkLabel(QtWidgets.QLabel):

    def __init__(self, parent, url):
        super(BookmarkLabel, self).__init__()
        self.parent = parent
        self.url = url
        self.tab_theme_unselected = None
        self.tab_theme_unselected_light = None
        self.layout = QtWidgets.QGridLayout()
        self.title = QtWidgets.QLabel(self)
        self.title.setText(self.url)
        self.layout.addWidget(self.title)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setGeometry(0,0,1,1)
        self.setLayout(self.layout)
        self.setAttribute(QtCore.Qt.WA_Hover)

    def mousePressEvent(self, event):
        self.parent.parent.parent.parent.ui.label_panel.addTab(self.url)
        self.parent.parent.parent.parent.ui.label_panel.closeStartPage()

    def enterEvent(self, event):
        self.setStyleSheet("QLabel{" + self.tab_theme_unselected_light + "}")
        # self.title.setStyleSheet("QLabel{" + self.tab_theme_unselected_light + "}")

    def leaveEvent(self, event):
        self.setStyleSheet("QLabel{" + self.tab_theme_unselected + "}")
        # self.title.setStyleSheet("QLabel{" + self.tab_theme_unselected + "}")