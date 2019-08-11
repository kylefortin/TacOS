"""
==========================
TacOS OBA Configuration UI
==========================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

from Objects.OBAs import OBAs
from Objects.Logger import Logger
from AnyQt.QtWidgets import QWidget, QTableWidget,\
    QTableWidgetItem, QPushButton, QVBoxLayout,\
    QHBoxLayout, QAbstractItemView, QHeaderView,\
    QMessageBox
from AnyQt.QtCore import Qt, pyqtSignal
from UI.AddOBAUI import AddOBAUI
from UI.EditOBAUI import EditOBAUI


class OBAConfigUI(QWidget, OBAs):

    keyPressed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(OBAConfigUI, self).__init__()
        self.parent = parent
        self.title = 'OnBoard Air Configuration'
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self._logger = Logger('obaConfig', "UI : OBAConfig")

        # Create layout
        self._plus = QPushButton('+', self)
        self._plus.clicked.connect(self.__createOBA)
        self._minus = QPushButton('-', self)
        self._minus.clicked.connect(self.__destroyOBA)
        panel = QWidget(self)
        panel.layout = QHBoxLayout(panel)
        panel.layout.setAlignment(Qt.AlignRight)
        panel.layout.addWidget(self._plus)
        panel.layout.addWidget(self._minus)
        self.layout.addWidget(panel)
        self._obaList = QTableWidget(0, 5, self)
        self._obaList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._obaList.setHorizontalHeaderLabels(['Name', 'Output Pin', 'Momentary', 'Enabled', 'Icon'])
        self._obaList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keyPressed.connect(self.__onKey)
        self.layout.addWidget(self._obaList)
        self._editBtn = QPushButton('Edit', self)
        self._editBtn.clicked.connect(self.__editOBA)
        self.layout.addWidget(self._editBtn)
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__closeBtnAction)
        self.layout.addWidget(self._closeBtn)

        # Load config files
        self.load()

        msg = 'TacOS OBAConfig UI initialized successfully'
        self._logger.log(msg)

    def keyPressEvent(self, event):
        super(OBAConfigUI, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def refresh(self):
        self.__init__(parent=self.parent)

    def addOBA(self, oba):
        super(OBAConfigUI, self).addOBA(oba)
        idx = self._obaList.rowCount()
        self._obaList.setRowCount(idx + 1)
        self.__setRow(idx, oba)

    def editOBA(self, oba, idx):
        super(OBAConfigUI, self).editOBA(oba, idx)
        self.__editRow(idx, oba)

    def createOBA(self, oba):
        super(OBAConfigUI, self).createOBA(oba)
        idx = self._obaList.rowCount()
        self._obaList.setRowCount(idx + 1)
        self.__setRow(idx, oba)

    def rmOBA(self, index):
        super(OBAConfigUI, self).rmOBA(index)
        self._obaList.removeRow(index)

    def __onKey(self, key):
        if key == Qt.Key_Escape:
            self._obaList.clearSelection()

    def __setRow(self, idx, oba):
        c = 0
        for item in [oba.name, str(oba.outputPin), str(oba.momentary),
                     str(oba.enabled), oba.icon]:
            tableItem = QTableWidgetItem(item)
            tableItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._obaList.setItem(idx, c, tableItem)
            c += 1

    def __editRow(self, idx, oba):
        map = {
            0: oba.name,
            1: str(oba.outputPin),
            2: str(oba.momentary),
            3: str(oba.enabled),
            4: oba.icon
        }
        for col in map.keys():
            tableItem = self._obaList.item(idx, col)
            tableItem.setText(map[col])

    def __createOBA(self):
        # Create Edit UI and add to tabs
        ui = AddOBAUI(availablePins=self.parent.availablePins(), parent=self)
        ui.setParent(self)
        i = self.parent.tabs.addTab(ui, 'Create OnBoard Air Element')
        self.parent.tabs.setCurrentIndex(i)
        self.parent.disableConfigButtons()

    def __destroyOBA(self):
        rows = self._obaList.selectedIndexes()
        names = []
        for i in rows:
            names.append(self._obaList.item(i.row(), 0))
        for name in names:
            for n in range(self._obaList.rowCount()):
                if self._obaList.item(n, 0) == name:
                    self.rmOBA(n)

    def __editOBA(self):
        sIdx = self._obaList.currentIndex().row()
        if sIdx not in [None, -1]:
            # Read selected row attributes
            sName = self._obaList.item(sIdx, 0).text()
            sPin = int(self._obaList.item(sIdx, 1).text())
            sMom = self._obaList.item(sIdx, 2).text() != 'False'
            sEnable = self._obaList.item(sIdx, 3).text() != 'False'
            sIcon = self._obaList.item(sIdx, 4).text()
            # Disable Config tab
            self.parent.tabs.setTabEnabled(self.parent.tabs.currentIndex(), False)
            # Create Edit UI and add to tabs
            ui = EditOBAUI(name=sName, outputPin=sPin, enabled=sEnable, icon=sIcon,
                            momentary=sMom, index=sIdx, availablePins=self.parent.availablePins(sPin),
                            parent=self)
            ui.setParent(self)
            i = self.parent.tabs.addTab(ui, 'Edit OnBoard Air Element')
            self.parent.tabs.setCurrentIndex(i)
            self.parent.disableConfigButtons()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Unable to Edit OBA Element')
            msgBox.setText('Please select an OBA element before editing.')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.exec_()

    def __closeBtnAction(self):
        self.save()
        if self.parent is not None:
            self.parent.tabs.removeTab(self.parent.tabs.currentIndex())
            self.parent.redrawOBAPanel(self.__formatOBA(), True)
            self.parent._configBtn.setVisible(True)

    def __formatOBA(self):
        i = 0
        r = {}
        for oba in self.obas:
            try:
                r[i] = {'name': oba.name,
                   'outputPin': oba.outputPin,
                   'momentary': oba.momentary,
                   'active': self.parent.OBAControlUI.obas[i]['active'],
                   'icon': oba.icon}
            except:
                r[i] = {'name': oba.name,
                        'outputPin': oba.outputPin,
                        'momentary': oba.momentary,
                        'active': False,
                        'icon': oba.icon}
            i += 1
        return r

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, name='', title=''):
        """
        Set the internal logger name and title
        :param name: The backend name of the logger.
        :type name: str
        :param title: The display title of the logger.
        :type title: str
        :return: None
        """
        if name != '':
            self._logger.name = name
        if title != '':
            self._logger.title = title
