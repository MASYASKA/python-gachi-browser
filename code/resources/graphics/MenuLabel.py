from PyQt5 import QtWidgets

class MenuLabel(QtWidgets.QLabel):

    def __init__(self, parent, x, y, width, height):
        super(MenuLabel, self).__init__(parent=parent)
        self.parent = parent
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(r"QLabel{ background-color : white}")
        self.setVisible(False)
        self.visible = False

    def setMenu(self):
        if self.visible:
            self.setVisible(False)
            self.visible = False
        else:
            self.setVisible(True)
            self.visible = True