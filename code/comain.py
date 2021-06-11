from PyQt5 import QtWidgets, QtGui, QtCore
import sys; sys.path += ['E://0//git//python-gachi-browser//code//resources']
import graphics


class MainView(QtWidgets.QGraphicsView):

    transformed = QtCore.pyqtSignal()

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
            self.width, self.height = 1080, 720
            self.setGeometry(250, 250, self.width, self.height)
            self.setScene(self.scene)
            self.maximized = False
            self.transformed.emit()
        else:
            self.width, self.height = 1920, 1040
            self.setGeometry(0, 0, self.width, self.height)
            self.setScene(self.scene)
            self.maximized = True
            self.transformed.emit()

class MainScene(QtWidgets.QGraphicsScene):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent, ui_class):
        super(MainScene, self).__init__()
        self.parent = parent
        self.width, self.height = parent.width, parent.height
        self.setSceneRect(0, 0, self.parent.width-2, self.parent.height-2)
        self.view = parent
        self.widget = MainWidget(self)
        self.widget.ui = ui_class()
        self.widget.scene = self
        self.widget.ui.setupUi(self.widget)
        self.addWidget(self.widget)
        self.connecting()

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        # self.widget.ui.button_sex.clicked.connect(self.button_sex_handler)
        self.widget.ui.label_panel.button_close.clicked.connect(self.view.close)
        self.widget.ui.label_panel.button_roll.clicked.connect(self.view.showMinimized)
        self.widget.ui.label_panel.button_scale.clicked.connect(self.view.showMiximazed)

    def transform(self):
        print('MainScene here!')
        self.width, self.height = self.parent.width-2, self.parent.height-2
        self.setSceneRect(0, 0, self.width, self.height)
        self.transformed.emit()

class MainWidget(QtWidgets.QWidget):

    transformed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(MainWidget, self).__init__()
        self.parent = parent
        self.width, self.height = parent.width, parent.height
        self.connecting()

    def connecting(self):
        self.parent.transformed.connect(self.transform)

    def transform(self):
        print('MainWidget here!')
        self.width, self.height = self.parent.width, self.parent.height
        self.setGeometry(0, 0, self.width, self.height)
        self.transformed.emit()


app = QtWidgets.QApplication(sys.argv)
view = MainView()
view.show()

sys.exit(app.exec_())