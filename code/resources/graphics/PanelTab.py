from PyQt5 import QtWidgets, QtCore, QtTest
from PushedLabel import *

class PanelTab(QtWidgets.QLabel):

    transformed = QtCore.pyqtSignal()
    # clicked = QtCore.pyqtSignal()

    def __init__(self, parent, count):
        super(PanelTab, self).__init__(parent=parent)
        # params
        
        self.parent = parent
        self.id = f'tab_{count}'
        self.position = count
        self.current_text = ''
        if count > 0: self.x = 140*count
        else: self.x = 0
        self.y = 0
        self.pos_x, self.pos_y = self.x, self.y
        self.width, self.height = 140, 25
        
        # items

        self.title = QtWidgets.QLabel(self)
        self.icon = QtWidgets.QLabel(self)
        self.button_tab_close = PushedLabel(self, "resources//images//button_tab_close_black.png", 115, 0, 25, 25)
        font = self.title.font()
        
        # calls

        self.title.setText('Loading...')
        font.setPixelSize(13); self.title.setFont(font)
        self.title.setGeometry(25, 0, 130, 25)
        self.icon.setGeometry(5, 3, 18, 18)
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.connecting()

    # helper functions

    def delete(self):
        self.deleteLater()
        self.scene.deleteLater()
        self.scene.engine.deleteLater()
        del self.scene.engine
        del self.scene
        del self.parent.tab_dict[self.id]
        del self

    def setSelected(self):
        self.selected = True
        self.setStyleSheet("QLabel{" + self.parent.tab_theme_selected + "}")
        self.title.setStyleSheet(r"QLabel{ color : white; }")
        self.button_tab_close.setPixmap(QtGui.QPixmap('resources//images//button_tab_close_white.png'))
        self.button_tab_close.setVisible(True)

    def setUnselected(self):
        self.selected = False
        self.setStyleSheet("QLabel{" + self.parent.tab_theme_unselected + "}")
        self.title.setStyleSheet(r"QLabel{ color: black; }")
        self.button_tab_close.setPixmap(QtGui.QPixmap('resources//images//button_tab_close_black.png'))
        self.button_tab_close.setVisible(False)

    def setPageName(self):
        title = self.scene.engine.page().title()
        self.title.setText(title)
        self.setToolTip(title)
        QtTest.QTest.qWait(3000)
        try:
            icon = self.scene.engine.page().icon()
            self.icon.setPixmap(icon.pixmap(QtCore.QSize(15, 15)))
        except:
            pass


    # events

    def enterEvent(self, event):
        if self.selected:
            pass
        else:
            self.setStyleSheet("QLabel{" + self.parent.tab_theme_unselected_light + "}")
            self.button_tab_close.setVisible(True)

    def leaveEvent(self, event):
        if self.selected:
            pass
        else:
            self.setStyleSheet("QLabel{" + self.parent.tab_theme_unselected + "}")
            self.button_tab_close.setVisible(False)

    def mousePressEvent(self, event):
        self.parent.openTab(self)
        self.press_event_coord_x = event.globalPos().x()

    def mouseMoveEvent(self, event):
        self.move_event_coord_x = event.globalPos().x()
        diff_x = self.move_event_coord_x - self.press_event_coord_x
        self.setGeometry(self.x+diff_x, self.y, self.width, self.height)
        if diff_x > self.width:
            self.parent.moveTabForward(self)
        if diff_x < -self.width:
            self.parent.moveTabBack(self)

    def mouseReleaseEvent(self, event):
        self.parent.refresh()

    # required functions

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.button_tab_close.clicked.connect(self.parent.closeTab)

    def transform(self):
        print('PanelTab here!')
        self.button_tab_close.setGeometry(self.width-25, 0, 25, 25)
        self.transformed.emit()