"""
=================
TacOS AddLight UI
=================

Extends the TacOS Light class to provide a UI to configure a Light in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QPushButton,\
    QCheckBox, QComboBox, QLabel,\
    QHBoxLayout, QVBoxLayout
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.Light import Light
from Objects.LineEdit import LineEdit


class AddLightUI(QWidget):

    def __init__(self, parent):
        super(AddLightUI, self).__init__()
        self.title = 'Create Lighting Element'
        self.setLayout(QVBoxLayout(self))
        self.parent = parent
        self.light = Light(name='', outputPin=0, enabled=False, icon=Config.faIcon('lightbulb'), strobe=False)
        self._nameControl = LineEdit('Name', self)
        self._nameControl.kb.connect(self.showOSK)
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for _pin in self.parent.availablePins():
            self._outputPinControl.addItem(str(_pin))
        self._outputPinControl.setCurrentIndex(self._outputPinControl.findText(str(self.light.outputPin)))
        self._enabledControl = QCheckBox('Enabled', self)
        self._iconControlLabel = QLabel('Icon', self)
        self._iconControl = QComboBox(self)
        for _key in Config.icons['lights'].keys():
            icon = Config.icon('lights', _key)
            self._iconControl.addItem(icon['name'], _key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        self._strobeControl = QCheckBox('Strobe', self)
        self._addLightBtn = QPushButton('Add Lighting Element', self)
        self._addLightBtn.clicked.connect(self.__createLightBtnAction)
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)

        _layout = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_enabledControl', '_strobeControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_addLightBtn', '_cancelBtn']
        ]

        for _list in _layout:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            _panel.layout().setAlignment(Qt.AlignCenter)
            for _control in _list:
                _panel.layout().addWidget(eval('self.%s' % _control))
            self.layout().addWidget(_panel)

    def __createLightBtnAction(self):
        self.light.name = self._nameControl.text()
        self.light.outputPin = int(self._outputPinControl.currentText())
        self.light.enabled = self._enabledControl.isChecked()
        self.light.icon = self._iconControl.currentData()
        self.light.strobe = self._strobeControl.isChecked()
        self.parent.lights.addLight(self.light)
        self.parent.lights.save()
        self.parent.loadUI('config_light')
        self.parent.enableConfigButtons()

    def __cancel(self):
        self.parent.loadUI('config_light')
        self.parent.enableConfigButtons()

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
