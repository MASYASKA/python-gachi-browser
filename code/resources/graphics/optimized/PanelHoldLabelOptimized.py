# structure
import sys
sys.path += ['E://0//git//python-gachi-browser//code//resources//graphics']
import PanelHoldLabel as PanelHoldLabel_old

class PanelHoldLabel(PanelHoldLabel_old.PanelHoldLabel):

    def openTab(self, tab):
        self.view_current_page.setScene(tab.scene)
        self.current_tab = tab
        self.refresh()
        self.edit_searchLine.line_edit.setEditTitle()
        self.edit_searchLine.line_edit_title.setVisible(True)
        self.edit_searchLine.line_edit.setText('')
        self.edit_searchLine.line_edit.setPlaceholderText("")

    def closeTab(self):
        tab = self.sender().parent
        for index in range(len(self.tab_lst)):
            if self.tab_lst[index] is tab:
                self.tab_lst.pop(index)
                break
        tab.delete()
        self.tab_count -= 1
        self.refresh()

    def connecting(self):
        self.parent.transformed.connect(self.transform)
        self.button_setStartPage.clicked.connect(self.addTab)
