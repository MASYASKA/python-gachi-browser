from PyQt5 import QtWidgets, QtCore

class SearchLine(QtWidgets.QLabel):

    def __init__(self, parent):
        super(SearchLine, self).__init__(parent=parent)
        self.parent = parent
        self.width, self.height = 950, 20
        self.x, self.y = 93, 30
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet("QLabel{border-radius: 3px; background-color: white;}")
        self.line_edit = SearchLineEdit(self)

    def load(self):
        self.parent.load_current_page()


class SearchLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent=parent)
        self.parent = parent
        self.setGeometry(QtCore.QRect(15, 1, 920, 18))
        self.setPlaceholderText("Enter request or address")
        self.setStyleSheet("QLineEdit{border: white;}")
        font = self.font(); font.setPointSize(10)
        self.setFont(font)

    # events
 
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.load()
            self.parent.parent.current_tab.current_text = self.text()
        else:
            super(SearchLineEdit, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        print('here we go!')
        super(SearchLineEdit, self).mousePressEvent(event)