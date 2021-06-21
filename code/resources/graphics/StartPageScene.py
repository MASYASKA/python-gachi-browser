from PyQt5 import QtWidgets, QtCore
from PushedLabel import *


class StartPageScene(QtWidgets.QGraphicsScene):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, panel):
        super(StartPageScene, self).__init__()
        # params
        self.parent = parent
        self.panel = panel
        self.x, self.y, self.width, self.height = 0, 0,  parent.width-2, parent.height-2
        # items
        self.widget = SceneMainWidget(self)
        # calls 
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

        self.button_addBookmark = PushedLabel(self, 'resources//images//button_add_bookmark.png', self.width-80-25, 285, 25, 25)
        self.edit_addBookmark = BookmarkEdit(self)
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

        self.connecting()

    # bookmarks

    def addBookmark(self, url):
        bookmark = BookmarkLabel(self, url)
        self.widget_layout.layout.addWidget(bookmark, self.line, self.column)
        self.bookmark_lst += [bookmark]
        if self.column > 4:
            self.column = 0
            self.line += 1
        else:
            self.column += 1

    def deleteBookmark(self, bookmark):
        bookmark.deleteLater()
        del self.bookmark_lst[self.bookmark_lst.index(bookmark)]
        # delete from layer 
        # resort gridlayout
        # вычитать колонку и строку
        if self.column < 1:
            self.line -= 1
            self.column = 4
        else:
            self.column -= 1
        self.widget_layout.layout.removeWidget(bookmark)
        del bookmark

    # helper

    def setTheme(self, main):
        self.widget_layout.setStyleSheet("QWidget{" + self.parent.panel.tab_theme_unselected
                                            + "}")
        for qbookmark in self.bookmark_lst:
            qbookmark.setStyleSheet("Qlabel{" + self.parent.panel.tab_theme_selected + "border-radius: 5px;}")
            qbookmark.tab_theme_unselected = self.parent.panel.tab_theme_unselected
            qbookmark.tab_theme_unselected_light = self.parent.panel.tab_theme_unselected_light

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.button_addBookmark.clicked.connect(self.edit_addBookmark.setBookmarkEdit)

    def transform(self):
        self.width, self.height = self.parent.width, self.parent.height
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.widget_layout.setGeometry(80, 25, self.width-80-80, 260)
        self.button_addBookmark.setGeometry(self.width-80-25, 285, 25, 25)


class BookmarkLabel(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, url):
        super(BookmarkLabel, self).__init__()
        self.parent = parent
        self.url = url
        self.tab_theme_unselected = self.parent.parent.panel.tab_theme_unselected
        self.tab_theme_unselected_light = self.parent.parent.panel.tab_theme_unselected_light

        self.layout = QtWidgets.QGridLayout()
        self.layout.title_layout = QtWidgets.QGridLayout()
        self.layout.button_layout = QtWidgets.QGridLayout()
        self.title = QtWidgets.QLabel(self)
        self.button_close = PushedLabel(self, "resources//images//button_tab_close_black.png", 15, 5, 20, 20)

        self.title.setText(self.url)
        self.layout.title_layout.addWidget(self.title)
        self.layout.title_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.button_layout.addWidget(self.button_close)
        self.layout.button_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addLayout(self.layout.title_layout, 1, 1)
        self.layout.addLayout(self.layout.button_layout, 1, 2)

        self.button_close.setVisible(False)
        self.setGeometry(0,0,1,1)
        self.setLayout(self.layout)
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.connecting()

    # required functions

    def connecting(self):
        self.button_close.clicked.connect(self.suicide)

    def suicide(self):
        self.parent.deleteBookmark(self)

    # events

    def mousePressEvent(self, event):
        self.parent.parent.panel.addTab(self.url)
        self.parent.parent.panel.closeStartPage()

    def enterEvent(self, event):
        self.setStyleSheet("QLabel{" + self.tab_theme_unselected_light + "}")
        self.button_close.setVisible(True)
        # self.title.setStyleSheet("QLabel{" + self.tab_theme_unselected_light + "}")

    def leaveEvent(self, event):
        self.setStyleSheet("QLabel{" + self.tab_theme_unselected + "}")
        self.button_close.setVisible(False)
        # self.title.setStyleSheet("QLabel{" + self.tab_theme_unselected + "}")


class BookmarkEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(BookmarkEdit, self).__init__(parent=parent)
        self.parent = parent
        self.visible = False
        self.x, self.y, self.width, self.height = parent.width-80-150, 310, 150, 15

        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setVisible(self.visible)
        self.setPlaceholderText("Enter website url")

    def setBookmarkEdit(self):
        if self.visible:
            self.visible = False
            self.setVisible(self.visible)
        else:
            self.visible = True
            self.setVisible(self.visible)

    # events

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.addBookmark(self.text())
            self.setVisible(False)
        else:
            super(BookmarkEdit, self).keyPressEvent(event)

    def focusOutEvent(self, event):
        self.visible = False
        self.setVisible(self.visible)