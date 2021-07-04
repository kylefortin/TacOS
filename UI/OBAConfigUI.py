"""
==========================
TacOS OBA Configuration UI
==========================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

from Objects.Logger import Logger
from AnyQt.QtWidgets import QWidget, QTableWidget, \
    QTableWidgetItem, QPushButton, QVBoxLayout, \
    QHBoxLayout, QAbstractItemView, QHeaderView, \
    QMessageBox, QMainWindow
from AnyQt.QtCore import Qt, pyqtSignal
from UI.AddOBAUI import AddOBAUI
from UI.EditOBAUI import EditOBAUI


class OBAConfigUI(QWidget):
    keyPressed = pyqtSignal(int)

    def __init__(self, obas, parent):
        super(OBAConfigUI, self).__init__()
        self.title = 'OnBoard Air Configuration'
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignCenter)
        self.parent = parent
        self.obas = obas

        # Init logger
        self.logger = Logger('obaConfig', "UI : OBAConfig")

        # Create layout
        self._plus = QPushButton('+', self)
        self._plus.clicked.connect(self.__createOBA)
        self._minus = QPushButton('-', self)
        self._minus.clicked.connect(self.__destroyOBA)
        _panel = QWidget(self)
        _panel.layout = QHBoxLayout(_panel)
        _panel.layout.setAlignment(Qt.AlignRight)
        _panel.layout.addWidget(self._plus)
        _panel.layout.addWidget(self._minus)
        self.layout().addWidget(_panel)
        self._obaList = QTableWidget(0, 5, self)
        self._obaList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._obaList.setHorizontalHeaderLabels(['Name', 'Output Pin', 'Momentary', 'Enabled', 'Icon'])
        self._obaList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keyPressed.connect(self.__onKey)
        self.layout().addWidget(self._obaList)
        self._editBtn = QPushButton('Edit', self)
        self._editBtn.clicked.connect(self.__editOBA)
        self.layout().addWidget(self._editBtn)
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__closeBtnAction)
        self.layout().addWidget(self._closeBtn)

        # Populate table
        for _oba in self.obas:
            _i = self._obaList.rowCount()
            self._obaList.setRowCount(_i + 1)
            for _c, _item in enumerate([_oba.name, str(_oba.outputPin), str(_oba.momentary),
                                        str(_oba.enabled), _oba.icon]):
                _tblItem = QTableWidgetItem(_item)
                _tblItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._obaList.setItem(_i, _c, _tblItem)

    def keyPressEvent(self, event):
        super(OBAConfigUI, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def __onKey(self, key):
        if key == Qt.Key_Escape:
            self._obaList.clearSelection()

    def __createOBA(self):
        self.parent.loadUI('create_oba')

    def __destroyOBA(self):
        items = self._obaList.selectedIndexes()
        rows = []
        for i in items:
            if i.row() not in rows:
                rows.append(i.row())
        rows.sort(reverse=True)
        for row in rows:
            self.parent.obas.rmOBA(row)
        self.parent.obas.save()
        self.parent.loadUI('config_oba')

    def __editOBA(self):
        sIdx = self._obaList.currentIndex().row()
        if sIdx not in [None, -1]:
            self.parent.loadUI("edit_oba", sIdx)
            self.parent.disableConfigButtons()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Unable to Edit OBA Element')
            msgBox.setText('Please select an OBA element before editing.')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.exec_()

    def __closeBtnAction(self):
        self.parent.loadUI('control_oba')
        self.parent.enableConfigButtons()
