"""
============================
TacOS Light Configuration UI
============================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

from Objects.Lights import Lights
from Objects.Logger import Logger
from AnyQt.QtWidgets import QWidget, QTableWidget, \
    QTableWidgetItem, QPushButton, QVBoxLayout, \
    QHBoxLayout, QAbstractItemView, QHeaderView, \
    QMessageBox
from AnyQt.QtCore import Qt, pyqtSignal
from UI.AddLightUI import AddLightUI
from UI.EditLightUI import EditLightUI


class LightConfigUI(QWidget, Lights):
    keyPressed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(LightConfigUI, self).__init__()
        self.parent = parent
        self.title = 'Lighting Configuration'
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self._logger = Logger('lightConfig', "UI : LightConfig", level='debug')

        # Create layout
        self._plus = QPushButton('+', self)
        self._plus.clicked.connect(self.__createLight)
        self._minus = QPushButton('-', self)
        self._minus.clicked.connect(self.__destroyLight)
        panel = QWidget(self)
        panel.layout = QHBoxLayout(panel)
        panel.layout.setAlignment(Qt.AlignRight)
        panel.layout.addWidget(self._plus)
        panel.layout.addWidget(self._minus)
        self.layout.addWidget(panel)
        self._lightsList = QTableWidget(0, 4, self)
        self._lightsList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._lightsList.setHorizontalHeaderLabels(['Name', 'Output Pin', 'Enabled', 'Icon'])
        self._lightsList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keyPressed.connect(self.__onKey)
        self.layout.addWidget(self._lightsList)
        self._editBtn = QPushButton('Edit', self)
        self._editBtn.clicked.connect(self.__editLight)
        self.layout.addWidget(self._editBtn)
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__closeBtnAction)
        self.layout.addWidget(self._closeBtn)

        # Load config files
        self.load()

        msg = 'TacOS LightConfig UI initialized successfully'
        self._logger.log(msg)

    def keyPressEvent(self, event):
        super(LightConfigUI, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def refresh(self):
        self.__init__(parent=self.parent)

    def addLight(self, light):
        super(LightConfigUI, self).addLight(light)
        idx = self._lightsList.rowCount()
        self._lightsList.setRowCount(idx + 1)
        self.__setRow(idx, light)

    def editLight(self, light, idx):
        super(LightConfigUI, self).editLight(light, idx)
        self.__editRow(idx, light)

    def createLight(self, light):
        super(LightConfigUI, self).createLight(light)
        idx = self._lightsList.rowCount()
        self._lightsList.setRowCount(idx + 1)
        self.__setRow(idx, light)

    def rmLight(self, index):
        super(LightConfigUI, self).rmLight(index)
        self._lightsList.removeRow(index)

    def __onKey(self, key):
        if key == Qt.Key_Escape:
            self._lightsList.clearSelection()

    def __setRow(self, idx, light):
        c = 0
        for item in [light.name, str(light.outputPin),
                     str(light.enabled), light.icon]:
            tableItem = QTableWidgetItem(item)
            tableItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._lightsList.setItem(idx, c, tableItem)
            c += 1

    def __editRow(self, idx, light):
        map = {
            0: light.name,
            1: str(light.outputPin),
            2: str(light.enabled),
            3: light.icon
        }
        for col in map.keys():
            tableItem = self._lightsList.item(idx, col)
            tableItem.setText(map[col])

    def __createLight(self):
        # Create Edit UI and add to tabs
        ui = AddLightUI(availablePins=self.parent.availablePins(), parent=self)
        ui.setParent(self)
        i = self.parent.tabs.addTab(ui, 'Create Lighting Element')
        self.parent.tabs.setCurrentIndex(i)
        self.parent.disableConfigButtons()

    def __destroyLight(self):
        rows = self._lightsList.selectedIndexes()
        names = []
        for i in rows:
            names.append(self._lightsList.item(i.row(), 0))
        for name in names:
            for n in range(self._lightsList.rowCount()):
                if self._lightsList.item(n, 0) == name:
                    self.rmLight(n)

    def __editLight(self):
        sIdx = self._lightsList.currentIndex().row()
        if sIdx not in [None, -1]:
            # Read selected row attributes
            sName = self._lightsList.item(sIdx, 0).text()
            sPin = int(self._lightsList.item(sIdx, 1).text())
            sEnable = self._lightsList.item(sIdx, 2).text() != 'False'
            sIcon = self._lightsList.item(sIdx, 3).text()
            # Disable Config tab
            self.parent.tabs.setTabEnabled(self.parent.tabs.currentIndex(), False)
            # Create Edit UI and add to tabs
            ui = EditLightUI(name=sName, outputPin=sPin, enabled=sEnable, icon=sIcon,
                             index=sIdx, availablePins=self.parent.availablePins(sPin), parent=self)
            ui.setParent(self)
            i = self.parent.tabs.addTab(ui, 'Edit Lighting Element')
            self.parent.tabs.setCurrentIndex(i)
            self.parent.disableConfigButtons()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Unable to Edit Lighting Element')
            msgBox.setText('Please select a Lighting element before editing.')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.exec_()

    def __closeBtnAction(self):
        self.save()
        if self.parent is not None:
            self.parent.tabs.removeTab(self.parent.tabs.currentIndex())
            self.parent.redrawLightPanel(self.__formatLight(), True)
            self.parent._configBtn.setVisible(True)

    def __formatLight(self):
        i = 0
        r = {}
        for light in self.lights:
            try:
                r[i] = {'name': light.name,
                        'outputPin': light.outputPin,
                        'active': self.parent.LightControlUI.lights[i]['active'],
                        'icon': light.icon}
            except:
                r[i] = {'name': light.name,
                        'outputPin': light.outputPin,
                        'active': False,
                        'icon': light.icon}
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
