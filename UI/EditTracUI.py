"""
=================
TacOS EditTrac UI
=================

Extends the TacOS Trac class to provide a UI to reconfigure Trac objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QPushButton, QCheckBox, \
    QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.LineEdit import LineEdit


class EditTracUI(QWidget):

    def __init__(self, trac, parent):
        super(EditTracUI, self).__init__()
        self.title = 'Edit TracControl Element'
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignCenter)
        self.parent = parent
        self.trac = trac

        # Init controls
        self._nameControl = LineEdit('Name', self)
        self._nameControl.setText(self.trac.name)
        self._nameControl.kb.connect(self.showOSK)
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for _pins in self.parent.availablePins():
            self._outputPinControl.addItem(str(_pins))
        for _i in range(self._outputPinControl.count()):
            if self._outputPinControl.itemText(_i) == str(self.trac.outputPin):
                self._outputPinControl.setCurrentIndex(_i)
                break
        self._enabledControl = QCheckBox('Enabled', self)
        self._enabledControl.setChecked(self.trac.enabled)
        self._iconControlLabel = QLabel('Icon Path', self)
        self._iconControl = QComboBox(self)
        for _key in Config.icons['tracControl'].keys():
            icon = Config.icon('tracControl', _key)
            self._iconControl.addItem(icon['name'], _key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        # Set combobox selection to icon variable
        for iconIdx in range(self._iconControl.count()):
            if self.trac.icon is not None and self._iconControl.itemData(iconIdx) == self.trac.icon:
                self._iconControl.setCurrentIndex(iconIdx)
                break
        self._saveBtn = QPushButton('Save', self)
        self._saveBtn.clicked.connect(self.__saveBtnAction)
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)
        _layout = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_saveBtn', '_cancelBtn']
        ]
        for _list in _layout:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            _panel.layout().setAlignment(Qt.AlignCenter)
            for _ctrl in _list:
                _panel.layout().addWidget(eval('self.%s' % _ctrl))
            self.layout().addWidget(_panel)

    def __saveBtnAction(self):
        self.trac.name = self._nameControl.text()
        self.trac.outputPin = int(self._outputPinControl.currentText())
        self.trac.enabled = self._enabledControl.isChecked()
        self.trac.icon = self._iconControl.currentData()
        self.parent.tracs.save()
        self.parent.loadUI('config_trac')

    def __cancel(self):
        self.parent.loadUI('config_trac')

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
