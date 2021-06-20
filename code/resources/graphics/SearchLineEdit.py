from PyQt5 import QtWidgets, QtCore
from PushedLabel import *

class SearchLine(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(SearchLine, self).__init__(parent=parent)
        self.parent = parent
        self.width, self.height = 950, 20
        self.x, self.y = 93, 30
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet("QLabel{border-radius: 3px; background-color: white;}")
        self.line_edit = SearchLineEdit(self)
        self.button_search = PushedLabel(self, 'resources//images//magnifer.png', 0, 0, 20, 20)
        self.line_edit_title = LineEditTitle(self)
        self.line_edit_title.setGeometry(self.width/2-((self.width/7)/2), 0, self.width/7, self.height)
        # self.edit_title.setStyleSheet("QLabel{background-color: black;}")
        self.searchSite = False

        self.connecting()

    def load(self):
        self.parent.load_current_page(self.searchSite)

    def changeSearch(self):
        if self.searchSite:
            self.button_search.setPixmap(QtGui.QPixmap('resources//images//magnifer.png'))
            self.searchSite = False
        else:
            self.button_search.setPixmap(QtGui.QPixmap('resources//images//planet.png'))
            self.searchSite = True

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.button_search.clicked.connect(self.changeSearch)

    def transform(self):
        self.line_edit_title.setGeometry(self.width/2-((self.width/7)/2), 0, self.width/7, self.height)
        self.transformed.emit()


class SearchLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent=parent)
        self.parent = parent
        self.panel = parent.parent
        self.x, self.y, self.width, self.height  = 22, 1, 913, 18


        self.setGeometry(QtCore.QRect(self.x, self.y, self.width, self.height))
        self.setPlaceholderText("Enter request or address")
        self.setStyleSheet("QLineEdit{background-color: white; border: white;}")
        font = self.font(); font.setPointSize(10)

    def setEditTitle(self):
        try:
            try:
                self.parent.line_edit_title.setText(self.parent.parent.current_tab.title.text())
            except RuntimeError:
                pass
        except AttributeError:
            self.parent.line_edit_title.setText(self.parent.parent.tab_stack[-1].title.text())

    def setTheme(self, main):
            self.parent.setStyleSheet("QLabel{" + main.tab_theme_unselected_light +\
                "border-radius:3px;" + "}")
            self.setStyleSheet("QLineEdit{" + main.tab_theme_unselected_light + "border-radius: 20px;" + "}")

    # events
 
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.load()
            self.parent.parent.current_tab.current_text = self.text()
            self.setTheme(self.panel)
        else:
            super(SearchLineEdit, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet("QLineEdit{border: white;}")
        self.parent.setStyleSheet("QLabel{border-radius: 3px; background-color: white;}")
        super(SearchLineEdit, self).mousePressEvent(event)


    def focusOutEvent(self, event):
        self.setTheme(self.panel)
        self.parent.line_edit_title.visible = True
        self.parent.line_edit_title.setVisible(self.parent.line_edit_title.visible)
        try:
            self.parent.parent.current_tab.current_text = self.text()
        except AttributeError:
            pass
        self.setText('')
        self.setPlaceholderText("")
        super(SearchLineEdit, self).focusOutEvent(event)


    def focusInEvent(self, event):
        self.parent.line_edit_title.visible = False
        self.parent.line_edit_title.setVisible(self.parent.line_edit_title.visible)
        try:
            self.setText(self.parent.parent.current_tab.current_text)
        except AttributeError:
            pass
        self.setPlaceholderText("Enter request or address")
        super(SearchLineEdit, self).focusInEvent(event)

class LineEditTitle(QtWidgets.QLabel):

    def __init__(self, parent):
        super(LineEditTitle, self).__init__(parent=parent)
        self.parent = parent
        self.x, self.y, self.width, self.height = parent.width/2-((parent.width/7)/2), 0, parent.width/7, parent.height
        self.visible = True
        self.connecting()

    def connecting(self):
        self.parent.parent.transformed.connect(self.transform)

    def transform(self):
        self.x, self.y, self.width, self.height = self.parent.width/2-((self.parent.width/7)/2), 0, self.parent.width/7, self.parent.height
        self.setGeometry(self.x, self.y, self.width, self.height)

    def mousePressEvent(self, event):
        self.parent.focusInEvent(QtGui.QFocusEvent(QtCore.QEvent(QtCore.QEvent.Type()).Type.MouseButtonPress, 0))
        self.parent.line_edit_title.visible = not self.parent.line_edit_title.visible # change True/False
        self.parent.line_edit_title.setVisible(self.parent.line_edit_title.visible)