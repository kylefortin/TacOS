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
from Objects.OBA import OBA
from Objects.LineEdit import LineEdit


class EditOBAUI(QWidget):

    def __init__(self, **kwargs):
        # Init parent class
        super(EditOBAUI, self).__init__()
        # Assign keyword arguments
        self.parent = kwargs.get('parent', None)
        self.window = kwargs.get('window', None)
        self.name = kwargs.get('name', '')
        self.outputPin = kwargs.get('outputPin', 0)
        self.enabled = kwargs.get('enabled', True)
        self.icon = kwargs.get('icon', None)
        self.momentary = kwargs.get('momentary', False)
        self.index = kwargs.get('index', 0)
        availablePins = kwargs.get('availablePins', Config.outputPinList)
        # Init internal OBA object
        self._oba = OBA(name=self.name, outputPin=self.outputPin, enabled=self.enabled,
                        icon=self.icon, momentary=self.momentary)
        # Set window title
        self.title = 'Edit OBA Element'
        # Set window layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        # Init Name text control
        self._nameControl = LineEdit('Name', self)
        self._nameControl.setText(self.name)
        self._nameControl.kb.connect(self.showOSK)
        # Init Output Pin dropdown control
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for x in availablePins:
            self._outputPinControl.addItem(str(x))
        for i in range(self._outputPinControl.count()):
            # Set current index if matching outputPin attribute
            if self._outputPinControl.itemText(i) == str(self.outputPin):
                self._outputPinControl.setCurrentIndex(i)
                break
        # Destroy local variables
        del x, i
        # Init Momentary checkbox control and set value
        self._momentaryControl = QCheckBox('Momentary', self)
        self._momentaryControl.setChecked(self.momentary)
        # Init Enabled checkbox control and set value
        self._enabledControl = QCheckBox('Enabled', self)
        self._enabledControl.setChecked(self.enabled)
        # Init Icon dropdown control
        self._iconControlLabel = QLabel('Icon Path', self)
        self._iconControl = QComboBox(self)
        for key in Config.icons['oba'].keys():
            icon = Config.icon('oba', key)
            self._iconControl.addItem(icon['name'], key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        for i in range(self._iconControl.count()):
            # Set current index if matching icon attribute
            if self.icon is not None and self._iconControl.itemData(i) == self.icon:
                self._iconControl.setCurrentIndex(i)
                break
        del key, i
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
            ['_momentaryControl', '_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_saveBtn', '_cancelBtn']
        ]
        for l in layoutList:
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            panel.layout.setAlignment(Qt.AlignCenter)
            panel.layout.setSpacing(20)
            for ctrl in l:
                panel.layout.addWidget(eval('self.%s' % ctrl))
            self.layout.addWidget(panel)
        # Destroy local variables
        del l, ctrl

    def __saveBtnAction(self):
        # Write values back to internal OBA object
        self._oba.name = self._nameControl.text()
        self._oba.outputPin = int(self._outputPinControl.currentText())
        self._oba.enabled = self._enabledControl.isChecked()
        self._oba.icon = self._iconControl.currentData()
        self._oba.momentary = self._momentaryControl.isChecked()
        if self.parent is not None:
            # Close tab window and execute edit function
            self.parent.editOBA(self._oba, self.index)
        if self.window is not None:
            self.window.close()

    def __cancel(self):
        # Close window
        self.close()
        if self.parent is not None:
            self.parent.parent.refreshConfigPanels()
        if self.window is not None:
            self.window.close()

    def showOSK(self):
        self.window().dock.show()
        self.window().osk.rWidget = self._nameControl
