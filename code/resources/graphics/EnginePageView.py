from PyQt5 import QtWidgets, QtWebEngineWidgets

class ViewEnginePage(QtWebEngineWidgets.QWebEngineView):

    def __init__(self, parent):
        super(ViewEnginePage, self).__init__()
        self.parent = parent
        self.width, self.height = parent.width, parent.height
        self.setGeometry(0, 54, self.width, self.height)
        self.connecting()

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('ViewMainPage here!')
        self.width, self.height = self.parent.width, self.parent.height
        self.setGeometry(0, 54, self.width, self.height)