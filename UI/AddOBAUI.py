"""
=================
TacOS AddOBA UI
=================

Extends the TacOS OBA class to provide a UI to configure an OBA Element in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QPushButton,\
    QCheckBox, QComboBox, QLabel,\
    QHBoxLayout, QVBoxLayout
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.OBA import OBA
from Objects.LineEdit import LineEdit


class AddOBAUI(QWidget):

    def __init__(self, parent):
        super(AddOBAUI, self).__init__()
        self.title = 'Create OBA Element'
        self.setLayout(QVBoxLayout(self))
        self.parent = parent
        self.oba = OBA(name='', outputPin=0, enabled=False, icon=Config.icon('oba', 'airhose'), momentary=False)
        self._nameControl = LineEdit('Name', self)
        self._nameControl.kb.connect(self.showOSK)
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for _pin in self.parent.availablePins():
            self._outputPinControl.addItem(str(_pin))
        self._outputPinControl.setCurrentIndex(self._outputPinControl.findText(str(self.oba.outputPin)))
        self._momentaryControl = QCheckBox('Momentary', self)
        self._enabledControl = QCheckBox('Enabled', self)
        self._iconControlLabel = QLabel('Icon', self)
        self._iconControl = QComboBox(self)
        for _key in Config.icons['oba'].keys():
            icon = Config.icon('oba', _key)
            self._iconControl.addItem(icon['name'], _key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        self._addOBABtn = QPushButton('Add OBA Element', self)
        self._addOBABtn.clicked.connect(self.__createOBABtnAction)
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)
        _layout = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_momentaryControl', '_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_addOBABtn', '_cancelBtn']
        ]
        for _list in _layout:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            _panel.layout().setAlignment(Qt.AlignCenter)
            for _control in _list:
                _panel.layout().addWidget(eval('self.%s' % _control))
            self.layout().addWidget(_panel)

    def __createOBABtnAction(self):
        self.oba.name = self._nameControl.text()
        self.oba.outputPin = int(self._outputPinControl.currentText())
        self.oba.enabled = self._enabledControl.isChecked()
        self.oba.icon = self._iconControl.currentData()
        self.oba.momentary = self._momentaryControl.isChecked()
        self.parent.obas.addOBA(self.oba)
        self.parent.obas.save()
        self.parent.loadUI('config_oba')
        self.parent.enableConfigButtons()

    def __cancel(self):
        self.parent.loadUI('config_oba')
        self.parent.enableConfigButtons()

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
