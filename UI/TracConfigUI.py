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


class TracConfigUI(QWidget, Tracs):
    keyPressed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TracConfigUI, self).__init__()
        self.parent = parent
        self.title = 'TracControl Configuration'
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self._logger = Logger('tracConfig', "UI : TracConfig", level='debug')

        # Create layout
        self._plus = QPushButton('+', self)
        self._plus.clicked.connect(self.__createTrac)
        self._minus = QPushButton('-', self)
        self._minus.clicked.connect(self.__destroyTrac)
        panel = QWidget(self)
        panel.layout = QHBoxLayout(panel)
        panel.layout.setAlignment(Qt.AlignRight)
        panel.layout.addWidget(self._plus)
        panel.layout.addWidget(self._minus)
        self.layout.addWidget(panel)
        self._tracsList = QTableWidget(0, 4, self)
        self._tracsList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._tracsList.setHorizontalHeaderLabels(['Name', 'Output Pin', 'Enabled', 'Icon'])
        self._tracsList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keyPressed.connect(self.__onKey)
        self.layout.addWidget(self._tracsList)
        self._editBtn = QPushButton('Edit', self)
        self._editBtn.clicked.connect(self.__editTrac)
        self.layout.addWidget(self._editBtn)
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__closeBtnAction)
        self.layout.addWidget(self._closeBtn)

        # Load config files
        self.load()

        msg = 'TacOS TracConfig UI initialized successfully'
        self._logger.log(msg)

    def keyPressEvent(self, event):
        super(TracConfigUI, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def refresh(self):
        self.__init__(parent=self.parent)

    def addTrac(self, trac):
        super(TracConfigUI, self).addTrac(trac)
        idx = self._tracsList.rowCount()
        self._tracsList.setRowCount(idx + 1)
        self.__setRow(idx, trac)

    def editTrac(self, trac, idx):
        super(TracConfigUI, self).editTrac(trac, idx)
        self.__editRow(idx, trac)

    def createTrac(self, trac):
        super(TracConfigUI, self).createTrac(trac)
        idx = self._tracsList.rowCount()
        self._tracsList.setRowCount(idx + 1)
        self.__setRow(idx, trac)

    def rmTrac(self, index):
        super(TracConfigUI, self).rmTrac(index)
        self._tracsList.removeRow(index)

    def __onKey(self, key):
        if key == Qt.Key_Escape:
            self._tracsList.clearSelection()

    def __setRow(self, idx, trac):
        c = 0
        for item in [trac.name, str(trac.outputPin),
                     str(trac.enabled), trac.icon]:
            tableItem = QTableWidgetItem(item)
            tableItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._tracsList.setItem(idx, c, tableItem)
            c += 1

    def __editRow(self, idx, trac):
        map = {
            0: trac.name,
            1: str(trac.outputPin),
            2: str(trac.enabled),
            3: trac.icon
        }
        for col in map.keys():
            tableItem = self._tracsList.item(idx, col)
            tableItem.setText(map[col])

    def __createTrac(self):
        # Create Edit UI and add to tabs
        ui = AddTracUI(availablePins=self.parent.availablePins(), parent=self)
        ui.setParent(self)
        i = self.parent.tabs.addTab(ui, 'Create TracControl Element')
        self.parent.tabs.setCurrentIndex(i)
        self.parent.disableConfigButtons()

    def __destroyTrac(self):
        rows = self._tracsList.selectedIndexes()
        names = []
        for i in rows:
            names.append(self._tracsList.item(i.row(), 0))
        for name in names:
            for n in range(self._tracsList.rowCount()):
                if self._tracsList.item(n, 0) == name:
                    self.rmTrac(n)

    def __editTrac(self):
        sIdx = self._tracsList.currentIndex().row()
        if sIdx not in [None, -1]:
            # Read selected row attributes
            sName = self._tracsList.item(sIdx, 0).text()
            sPin = int(self._tracsList.item(sIdx, 1).text())
            sEnable = self._tracsList.item(sIdx, 2).text() != 'False'
            sIcon = self._tracsList.item(sIdx, 3).text()
            # Create window to show edit UI
            win = QMainWindow(self)
            # Create Edit UI and add to tabs
            ui = EditTracUI(name=sName, outputPin=sPin, enabled=sEnable, icon=sIcon,
                            index=sIdx, availablePins=self.parent.availablePins(sPin), parent=self,
                            window=win)
            ui.setParent(self)
            # Open window in fullscreen
            win.setCentralWidget(ui)
            if self.parent.prefs['startMaximized']:
                win.showFullScreen()
            else:
                win.show()
            self.parent.disableConfigButtons()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Unable to Edit TracControl Element')
            msgBox.setText('Please select a TracControl element before editing.')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.exec_()

    def __closeBtnAction(self):
        self.save()
        if self.parent is not None:
            self.parent.redrawTracPanel("Traction", self.__formatTrac())

    def __formatTrac(self):
        i = 0
        r = {}
        for trac in self.tracs:
            try:
                r[i] = {'name': trac.name,
                        'outputPin': trac.outputPin,
                        'active': self.parent.TracControlUI.tracs[i]['active'],
                        'icon': trac.icon}
            except:
                r[i] = {'name': trac.name,
                        'outputPin': trac.outputPin,
                        'active': False,
                        'icon': trac.icon}
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
