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

    def __init__(self, parent):
        super(AddTracUI, self).__init__()
        self.title = 'Create TracControl Element'
        self.setLayout(QVBoxLayout(self))
        self.parent = parent
        self.trac = Trac(name='', outputPin=0, enabled=False, icon=Config.icon('tracControl', 'rearDiff'), momentary=False)
        self._nameControl = LineEdit('Name', self)
        self._nameControl.kb.connect(self.showOSK)
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for _pin in self.parent.availablePins():
            self._outputPinControl.addItem(str(_pin))
        self._outputPinControl.setCurrentIndex(self._outputPinControl.findText(str(self.trac.outputPin)))
        self._enabledControl = QCheckBox('Enabled', self)
        self._iconControlLabel = QLabel('Icon', self)
        self._iconControl = QComboBox(self)
        for _key in Config.icons['tracControl'].keys():
            icon = Config.icon('tracControl', _key)
            self._iconControl.addItem(icon['name'], _key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        self._addTracBtn = QPushButton('Add TracControl Element', self)
        self._addTracBtn.clicked.connect(self.__createTracBtnAction)
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)
        _layout = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_addTracBtn', '_cancelBtn']
        ]
        for _list in _layout:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            _panel.layout().setAlignment(Qt.AlignCenter)
            for _control in _list:
                _panel.layout().addWidget(eval('self.%s' % _control))
            self.layout().addWidget(_panel)

    def __createTracBtnAction(self):
        self.trac.name = self._nameControl.text()
        self.trac.outputPin = int(self._outputPinControl.currentText())
        self.trac.enabled = self._enabledControl.isChecked()
        self.trac.icon = self._iconControl.currentData()
        self.parent.tracs.addTrac(self.trac)
        self.parent.tracs.save()
        self.parent.loadUI('config_trac')
        self.parent.enableConfigButtons()

    def __cancel(self):
        self.parent.loadUI('config_trac')
        self.parent.enableConfigButtons()

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
