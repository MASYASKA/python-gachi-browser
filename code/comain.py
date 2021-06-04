from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
import sys, graphics

class MainView(QtWidgets.QGraphicsView):

    def __init__(self):
        super(MainView, self).__init__()
        self.width, self.height = 1080, 720
        self.setGeometry(250, 250, self.width, self.height)
        self.setWindowTitle('Gachi Browser')
        self.scene = MainScene(self, graphics.Ui_Main)
        self.setScene(self.scene)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.maximized = False
        self.setSizePolicy(QtWidgets.QSizePolicy().horizontalPolicy(), QtWidgets.QSizePolicy().verticalPolicy())

    def showMiximazed(self):
        if self.maximized:
            self.setGeometry(250, 250, self.width, self.height)
            self.maximized = False
        else:
            # self.
            self.maximized = True

class MyEngineView(QtWebEngineWidgets.QWebEngineView):

    def __init__(self):
        super(MyEngineView, self).__init__()
        self.setGeometry(0, 54, 1080, 666)
        self.load(QtCore.QUrl('https://www.google.com/'))

class MainScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent, ui_class):
        super(MainScene, self).__init__()
        self.setSceneRect(0, 0,parent.width-2, parent.height-2)
        self.view = parent
        self.widget = QtWidgets.QWidget()
        self.widget.ui = ui_class()
        self.widget.ui.panel = graphics.PanelHoldButton(self.widget, self)
        self.widget.ui.setupUi(self.widget)
        self.addWidget(self.widget)
        self.page = MyEngineView()
        self.addWidget(self.page)
        self.connecting()

    def connecting(self):
        self.widget.ui.button_sex.clicked.connect(self.button_sex_handler)
        self.widget.ui.button_close.clicked.connect(self.view.close)
        self.widget.ui.button_roll.clicked.connect(self.view.showMinimized)
        self.widget.ui.button_scale.clicked.connect(self.view.showMiximazed)

    def button_sex_handler(self):
        if self.search_site:
            self.page.load(QtCore.QUrl(self.widget.ui.edit_searchLine.text()))
        else:
            self.page.load(QtCore.QUrl(f'https://www.google.com/search?q={self.widget.ui.edit_searchLine.text()}'))


class MyView(MainView):

    def __init__(self):
        super(MyView, self).__init__()


app = QtWidgets.QApplication(sys.argv)
view = MyView()
view.show()

sys.exit(app.exec_())