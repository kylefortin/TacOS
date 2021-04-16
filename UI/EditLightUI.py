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
from Objects.Light import Light
from Objects.LineEdit import LineEdit


class EditLightUI(QWidget):

    def __init__(self, **kwargs):
        # Init parent class
        super(EditLightUI, self).__init__()
        # Assign keyword arguments
        self.parent = kwargs.get('parent', None)
        self.window = kwargs.get('window', None)
        self.name = kwargs.get('name', '')
        self.outputPin = kwargs.get('outputPin', 0)
        self.enabled = kwargs.get('enabled', True)
        self.icon = kwargs.get('icon', None)
        self.strobe = kwargs.get('strobe', False)
        self.index = kwargs.get('index', 0)
        availablePins = kwargs.get('availablePins', Config.outputPinList)
        # Init internal Light object
        self._light = Light(name=self.name, outputPin=self.outputPin, enabled=self.enabled,
                            icon=self.icon, strobe=self.strobe)
        # Set window title
        self.title = 'Edit Lighting Element'
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
        # Init Enabled checkbox control and set value
        self._enabledControl = QCheckBox('Enabled', self)
        self._enabledControl.setChecked(self.enabled)
        # Init Icon dropdown control
        self._iconControlLabel = QLabel('Icon Path', self)
        self._iconControl = QComboBox(self)
        for key in Config.icons['lights'].keys():
            icon = Config.icon('lights', key)
            self._iconControl.addItem(icon['name'], key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        for i in range(self._iconControl.count()):
            # Set current index if matching icon attribute
            if self.icon is not None and self._iconControl.itemData(i) == self.icon:
                self._iconControl.setCurrentIndex(i)
                break
        # Destroy local variables
        del key, i
        # Init Strobe checkbox control and set value
        self._strobeControl = QCheckBox('Strobe', self)
        self._strobeControl.setChecked(self.strobe)
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
            panel.layout = QHBoxLayout(panel)
            panel.layout.setAlignment(Qt.AlignCenter)
            for ctrl in l:
                panel.layout.addWidget(eval('self.%s' % ctrl))
            self.layout.addWidget(panel)
        # Destroy local variables
        del l, ctrl

    def __saveBtnAction(self):
        # Write values back to internal Light object
        self._light.name = self._nameControl.text()
        self._light.outputPin = int(self._outputPinControl.currentText())
        self._light.enabled = self._enabledControl.isChecked()
        self._light.icon = self._iconControl.currentData()
        self._light.strobe = self._strobeControl.isChecked()
        if self.parent is not None:
            # Close tab window and execute edit function
            self.parent.editLight(self._light, self.index)
            self.parent.parent.refreshConfigPanels()
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
