"""
================
TacOS AddTrac UI
================

Extends the TacOS Trac class to provide a UI to configure a Trac in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QPushButton,\
    QCheckBox, QComboBox, QLabel,\
    QHBoxLayout, QVBoxLayout
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.Trac import Trac
from Objects.LineEdit import LineEdit


class AddTracUI(QWidget):

    def __init__(self, **kwargs):
        self.parent = kwargs.get('parent', None)
        availablePins = kwargs.get('availablePins', Config.outputPinList)
        super(AddTracUI, self).__init__()
        self.title = 'Create TracControl Element'
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._trac = Trac(name='', outputPin=0, enabled=False, icon=Config.icon('tracControl', 'rearDiff'), momentary=False)
        self._nameControl = LineEdit('Name', self)
        self._nameControl.kb.connect(self.showOSK)
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for x in availablePins:
            self._outputPinControl.addItem(str(x))
        self._outputPinControl.setCurrentIndex(self._outputPinControl.findText(str(self._trac.outputPin)))
        self._enabledControl = QCheckBox('Enabled', self)
        self._iconControlLabel = QLabel('Icon', self)
        self._iconControl = QComboBox(self)
        for key in Config.icons['tracControl'].keys():
            icon = Config.icon('tracControl', key)
            self._iconControl.addItem(icon['name'], key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        del key
        self._addTracBtn = QPushButton('Add TracControl Element', self)
        self._addTracBtn.clicked.connect(self.__createTracBtnAction)
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)

        layoutList = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_addTracBtn', '_cancelBtn']
        ]

        for l in layoutList:
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            panel.layout.setAlignment(Qt.AlignCenter)
            for ctrl in l:
                panel.layout.addWidget(eval('self.%s' % ctrl))
            self.layout.addWidget(panel)

    def __createTracBtnAction(self):
        self._trac.name = self._nameControl.text()
        self._trac.outputPin = int(self._outputPinControl.currentText())
        self._trac.enabled = self._enabledControl.isChecked()
        self._trac.icon = self._iconControl.currentData()
        if self.parent is not None:
            self.__closeTab()
            self.parent.createTrac(self._trac)

    def __cancel(self):
        self.close()
        if self.parent is not None:
            self.__closeTab()

    def __closeTab(self):
        self.parent.parent.tabs.removeTab(self.parent.parent.tabs.currentIndex())
        for i in range(self.parent.parent.tabs.count()):
            if 'Configure' in self.parent.parent.tabs.tabText(i):
                self.parent.parent.tabs.setTabEnabled(i, True)
                self.parent.parent.tabs.setCurrentIndex(i)

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
