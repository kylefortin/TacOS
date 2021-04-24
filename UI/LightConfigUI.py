"""
============================
TacOS Light Configuration UI
============================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

from Objects.Logger import Logger
from AnyQt.QtWidgets import QWidget, QTableWidget, \
    QTableWidgetItem, QPushButton, QVBoxLayout, \
    QHBoxLayout, QAbstractItemView, QHeaderView, \
    QMessageBox
from AnyQt.QtCore import Qt, pyqtSignal


class LightConfigUI(QWidget):
    keyPressed = pyqtSignal(int)

    def __init__(self, lights, parent):
        super(LightConfigUI, self).__init__()
        self.title = 'Lighting Configuration'
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignCenter)
        self.parent = parent
        self.lights = lights

        # Init logger
        self.logger = Logger('lightConfig', "UI : LightConfig", level='debug')

        # Create layout
        self._plus = QPushButton('+', self)
        self._plus.clicked.connect(self.__createLight)
        self._minus = QPushButton('-', self)
        self._minus.clicked.connect(self.__destroyLight)
        _panel = QWidget(self)
        _panel.setLayout(QHBoxLayout(_panel))
        _panel.layout().setAlignment(Qt.AlignRight)
        _panel.layout().addWidget(self._plus)
        _panel.layout().addWidget(self._minus)
        self.layout().addWidget(_panel)
        self._lightsList = QTableWidget(0, 5, self)
        self._lightsList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._lightsList.setHorizontalHeaderLabels(['Name', 'Output Pin', 'Enabled', 'Icon', 'Strobe'])
        self._lightsList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keyPressed.connect(self.__onKey)
        self.layout().addWidget(self._lightsList)
        self._editBtn = QPushButton('Edit', self)
        self._editBtn.clicked.connect(self.__editLight)
        self.layout().addWidget(self._editBtn)
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__closeBtnAction)
        self.layout().addWidget(self._closeBtn)

        # Populate table
        for _light in self.lights:
            _i = self._lightsList.rowCount()
            self._lightsList.setRowCount(_i+1)
            for _c, _item in enumerate([_light.name, str(_light.outputPin),
                          str(_light.enabled), _light.icon, str(_light.strobe)]):
                _tblItem = QTableWidgetItem(_item)
                _tblItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._lightsList.setItem(_i, _c, _tblItem)

    def keyPressEvent(self, event):
        super(LightConfigUI, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def __onKey(self, key):
        if key == Qt.Key_Escape:
            self._lightsList.clearSelection()

    def __createLight(self):
        self.parent.loadUI('create_light')

    def __destroyLight(self):
        items = self._lightsList.selectedIndexes()
        rows = []
        for i in items:
            if i.row() not in rows:
                rows.append(i.row())
        rows.sort(reverse=True)
        for row in rows:
            self.parent.lights.rmLight(row)
        self.parent.lights.save()
        self.parent.loadUI('config_light')

    def __editLight(self):
        sIdx = self._lightsList.currentIndex().row()
        if sIdx not in [None, -1]:
            self.parent.loadUI("edit_light", sIdx)
            self.parent.disableConfigButtons()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Unable to Edit Lighting Element')
            msgBox.setText('Please select a Lighting element before editing.')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.exec_()

    def __closeBtnAction(self):
        self.parent.loadUI('control_light')
        self.parent.enableConfigButtons()
