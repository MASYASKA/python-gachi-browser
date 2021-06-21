from PyQt5 import QtWidgets, QtCore

class ViewMainPage(QtWidgets.QGraphicsView):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(ViewMainPage, self).__init__(parent=parent)
        # params
        self.parent = parent
        self.width, self.height = 1080, 666
        # calls
        self.setGeometry(0, 54, self.width, self.height)
        self.connecting()

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('ViewMainPage here!')
        self.width, self.height = self.parent.width, self.parent.height-54
        self.setGeometry(0, 54, self.width, self.height)
        self.transformed.emit()