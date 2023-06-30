"""
==================================
TacOS TracControl Configuration UI
==================================

Extends the TacOS Tracs class to provide a UI to configure available Trac objects in the TacOS environment.

"""

from Objects.Tracs import Tracs
from Objects.Logger import Logger
from Objects import Config
from AnyQt.QtWidgets import QWidget, QTableWidget, \
    QTableWidgetItem, QPushButton, QVBoxLayout, \
    QHBoxLayout, QAbstractItemView, QHeaderView, \
    QMessageBox, QMainWindow
from AnyQt.QtCore import Qt, pyqtSignal
from UI.AddTracUI import AddTracUI
from UI.EditTracUI import EditTracUI


class TracConfigUI(QWidget):
    keyPressed = pyqtSignal(int)

    def __init__(self, parent):
        super(TracConfigUI, self).__init__()
        self.title = 'TracControl Configuration'
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignCenter)
        self.parent = parent
        self.tracs = self.parent.tracs

        # Init logger
        self.logger = Logger('tracConfig', "UI : TracConfig", level='debug')

        # Create layout
        self._plus = QPushButton('+', self)
        self._plus.clicked.connect(self.__createTrac)
        self._minus = QPushButton('-', self)
        self._minus.clicked.connect(self.__destroyTrac)
        _panel = QWidget(self)
        _panel.layout = QHBoxLayout(_panel)
        _panel.layout.setAlignment(Qt.AlignRight)
        _panel.layout.addWidget(self._plus)
        _panel.layout.addWidget(self._minus)
        self.layout().addWidget(_panel)
        self._tracsList = QTableWidget(0, 4, self)
        self._tracsList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._tracsList.setHorizontalHeaderLabels(['Name', 'Output Pin', 'Enabled', 'Icon'])
        self._tracsList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keyPressed.connect(self.__onKey)
        self.layout().addWidget(self._tracsList)
        self._editBtn = QPushButton('Edit', self)
        self._editBtn.clicked.connect(self.__editTrac)
        self.layout().addWidget(self._editBtn)
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__closeBtnAction)
        self.layout().addWidget(self._closeBtn)

        # Populate table
        for _trac in self.tracs.tracs:
            _i = self._tracsList.rowCount()
            self._tracsList.setRowCount(_i + 1)
            for _c, _item in enumerate([_trac.name, str(_trac.outputPin),
                                        str(_trac.enabled), _trac.icon]):
                _tblItem = QTableWidgetItem(_item)
                _tblItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._tracsList.setItem(_i, _c, _tblItem)

    def keyPressEvent(self, event):
        super(TracConfigUI, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def __onKey(self, key):
        if key == Qt.Key_Escape:
            self._tracsList.clearSelection()

    def __createTrac(self):
        self.parent.loadUI('create_trac')

    def __destroyTrac(self):
        items = self._tracsList.selectedIndexes()
        rows = []
        for i in items:
            if i.row() not in rows:
                rows.append(i.row())
        rows.sort(reverse=True)
        for row in rows:
            self.tracs.rmTrac(row)
        self.tracs.save()
        self.parent.loadUI('config_trac')

    def __editTrac(self):
        sIdx = self._tracsList.currentIndex().row()
        if sIdx not in [None, -1]:
            self.parent.loadUI("edit_trac", sIdx)
            self.parent.disableConfigButtons()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Unable to Edit Traction Control Element')
            msgBox.setText('Please select a Traction Control element before editing.')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.exec_()

    def __closeBtnAction(self):
        self.parent.loadUI('control_trac')
        self.parent.enableConfigButtons()
