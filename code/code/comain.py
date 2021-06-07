from PyQt5 import QtWidgets, QtGui, QtCore
import sys; sys.path += ['E://0//git//python-gachi-browser//code//code//resources']
import graphics

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

    def showMiximazed(self):
        if self.maximized:
            self.setGeometry(250, 250, self.width, self.height)
            self.scene.widget.ui.setUiSize(self.width, self.height)
            self.scene.setSceneRect(0, 0, self.width-2, self.height-2)
            self.setScene(self.scene)
            self.maximized = False
        else:
            self.setGeometry(0, 0, 1920, 1040)
            self.scene.widget.ui.setUiSize(1920, 1040)
            self.scene.widget.setGeometry(0, 0, 1920, 1040)
            self.scene.setSceneRect(0, 0, 1920-2, 1040-2)
            self.setScene(self.scene)
            self.maximized = True

class MainScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent, ui_class):
        super(MainScene, self).__init__()
        self.setSceneRect(0, 0,parent.width-2, parent.height-2)
        self.view = parent
        self.widget = QtWidgets.QWidget()
        self.widget.ui = ui_class()
        self.widget.scene = self
        self.widget.ui.setupUi(self.widget)
        self.addWidget(self.widget)
        self.connecting()

    def connecting(self):
        self.widget.ui.button_sex.clicked.connect(self.button_sex_handler)
        self.widget.ui.button_close.clicked.connect(self.view.close)
        self.widget.ui.button_roll.clicked.connect(self.view.showMinimized)
        self.widget.ui.button_scale.clicked.connect(self.view.showMiximazed)

    def button_sex_handler(self):
        if self.widget.ui.button_searchCondition.search_site:
            self.widget.ui.label_panel.current_tab.scene.engine.load(QtCore.QUrl(self.widget.ui.edit_searchLine.text()))
        else:
            self.widget.ui.label_panel.current_tab.scene.engine.load(QtCore.QUrl(f'https://www.google.com/search?q={self.widget.ui.edit_searchLine.text()}'))


app = QtWidgets.QApplication(sys.argv)
view = MainView()
view.show()

sys.exit(app.exec_())