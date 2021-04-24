"""
================
TacOS EditOBA UI
================

Extends the TacOS OBA class to provide a UI to reconfigure OBA Element objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QPushButton, QCheckBox,\
    QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.LineEdit import LineEdit


class EditOBAUI(QWidget):

    def __init__(self, oba, parent):
        super(EditOBAUI, self).__init__()
        self.parent = parent
        self.oba = oba
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignCenter)

        # Init Name text control
        self._nameControl = LineEdit('Name', self)
        self._nameControl.setText(self.oba.name)
        self._nameControl.kb.connect(self.showOSK)
        # Init Output Pin dropdown control
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for _pin in self.parent.availablePins():
            self._outputPinControl.addItem(str(_pin))
        for _i in range(self._outputPinControl.count()):
            if self._outputPinControl.itemText(_i) == str(self.oba.outputPin):
                self._outputPinControl.setCurrentIndex(_i)
                break
        # Init Momentary checkbox control and set value
        self._momentaryControl = QCheckBox('Momentary', self)
        self._momentaryControl.setChecked(self.oba.momentary)
        # Init Enabled checkbox control and set value
        self._enabledControl = QCheckBox('Enabled', self)
        self._enabledControl.setChecked(self.oba.enabled)
        # Init Icon dropdown control
        self._iconControlLabel = QLabel('Icon Path', self)
        self._iconControl = QComboBox(self)
        for _key in Config.icons['oba'].keys():
            icon = Config.icon('oba', _key)
            self._iconControl.addItem(icon['name'], _key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        for _i in range(self._iconControl.count()):
            # Set current index if matching icon attribute
            if self.oba.icon is not None and self._iconControl.itemData(_i) == self.oba.icon:
                self._iconControl.setCurrentIndex(_i)
                break
        # Init Save button
        self._saveBtn = QPushButton('Save', self)
        self._saveBtn.clicked.connect(self.__saveBtnAction)
        # Init cancel button
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)
        # Assign control layout
        _layout = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_momentaryControl', '_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_saveBtn', '_cancelBtn']
        ]
        for _list in _layout:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            _panel.layout().setAlignment(Qt.AlignCenter)
            _panel.layout().setSpacing(20)
            for _control in _list:
                _panel.layout().addWidget(eval('self.%s' % _control))
            self.layout().addWidget(_panel)

    def __saveBtnAction(self):
        self.oba.name = self._nameControl.text()
        self.oba.outputPin = int(self._outputPinControl.currentText())
        self.oba.enabled = self._enabledControl.isChecked()
        self.oba.icon = self._iconControl.currentData()
        self.oba.momentary = self._momentaryControl.isChecked()
        self.parent.obas.save()
        self.parent.loadUI('config_oba')

    def __cancel(self):
        self.parent.loadUI('config_oba')

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
