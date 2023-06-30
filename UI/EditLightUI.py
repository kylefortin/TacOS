"""
=================
TacOS EditLight UI
=================

Extends the TacOS Light class to provide a UI to reconfigure Light objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QPushButton, QCheckBox, \
    QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.LineEdit import LineEdit


class EditLightUI(QWidget):

    def __init__(self, idx, parent):
        super(EditLightUI, self).__init__()
        self.title = 'Edit Lighting Element'
        self.parent = parent
        self.light = self.parent.lights.lights[idx]
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignCenter)

        # Init Name text control
        self._nameControl = LineEdit('Name', self)
        self._nameControl.setText(self.light.name)
        self._nameControl.kb.connect(self.showOSK)
        # Init Output Pin dropdown control
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for x in self.parent.availablePins(self.light):
            self._outputPinControl.addItem(str(x))
        for i in range(self._outputPinControl.count()):
            if self._outputPinControl.itemText(i) == str(self.light.outputPin):
                self._outputPinControl.setCurrentIndex(i)
                break
        del x, i
        # Init Enabled checkbox control and set value
        self._enabledControl = QCheckBox('Enabled', self)
        self._enabledControl.setChecked(self.light.enabled)
        # Init Icon dropdown control
        self._iconControlLabel = QLabel('Icon Path', self)
        self._iconControl = QComboBox(self)
        for key in Config.icons['lights'].keys():
            icon = Config.icon('lights', key)
            self._iconControl.addItem(icon['name'], key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        for i in range(self._iconControl.count()):
            if self.light.icon is not None and self._iconControl.itemData(i) == self.light.icon:
                self._iconControl.setCurrentIndex(i)
                break
        del key, i
        # Init Strobe checkbox control and set value
        self._strobeControl = QCheckBox('Strobe', self)
        self._strobeControl.setChecked(self.light.strobe)
        # Init Save button
        self._saveBtn = QPushButton('Save', self)
        self._saveBtn.clicked.connect(self.__saveBtnAction)
        # Init cancel button
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)
        # Assign control layout
        layoutList = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_enabledControl', '_strobeControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_saveBtn', '_cancelBtn']
        ]
        for l in layoutList:
            panel = QWidget(self)
            panel.setLayout(QHBoxLayout(panel))
            panel.layout().setAlignment(Qt.AlignCenter)
            for ctrl in l:
                panel.layout().addWidget(eval('self.%s' % ctrl))
            self.layout().addWidget(panel)
        # Destroy local variables
        del l, ctrl

    def __saveBtnAction(self):
        self.light.name = self._nameControl.text()
        self.light.outputPin = int(self._outputPinControl.currentText())
        self.light.enabled = self._enabledControl.isChecked()
        self.light.icon = self._iconControl.currentData()
        self.light.strobe = self._strobeControl.isChecked()
        self.parent.lights.save()
        self.parent.loadUI("config_light")

    def __cancel(self):
        self.parent.loadUI("config_light")

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
