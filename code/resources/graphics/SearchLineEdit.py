from PyQt5 import QtWidgets, QtCore

class SearchLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent=parent)
        self.parent = parent
        self.setGeometry(QtCore.QRect(93, 33, 950, 16))
        self.setStyleSheet(" QLineEdit{\n""    border-radius: 2px;\n""    border: 1px solid black;\n""}")

    # events

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.ui.label_panel.load_current_page()
        else:
            super(SearchLineEdit, self).keyPressEvent(event)