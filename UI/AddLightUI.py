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

    def __init__(self, **kwargs):
        self.parent = kwargs.get('parent', None)
        availablePins = kwargs.get('availablePins', Config.outputPinList)
        super(AddLightUI, self).__init__()
        self.title = 'Create Lighting Element'
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._light = Light(name='', outputPin=0, enabled=False, icon=Config.faIcon('lightbulb'), momentary=False)
        self._nameControl = LineEdit('Name', self)
        self._nameControl.kb.connect(self.showOSK)
        self._outputPinControlLabel = QLabel('Output Pin', self)
        self._outputPinControl = QComboBox(self)
        for x in availablePins:
            self._outputPinControl.addItem(str(x))
        self._outputPinControl.setCurrentIndex(self._outputPinControl.findText(str(self._light.outputPin)))
        self._enabledControl = QCheckBox('Enabled', self)
        self._iconControlLabel = QLabel('Icon', self)
        self._iconControl = QComboBox(self)
        for key in Config.icons['lights'].keys():
            icon = Config.icon('lights', key)
            self._iconControl.addItem(icon['name'], key)
            self._iconControl.setItemIcon(self._iconControl.count() - 1, QIcon(icon['path']))
        del key
        self._addLightBtn = QPushButton('Add Lighting Element', self)
        self._addLightBtn.clicked.connect(self.__createLightBtnAction)
        self._cancelBtn = QPushButton('Cancel', self)
        self._cancelBtn.clicked.connect(self.__cancel)

        layoutList = [
            ['_nameControl'],
            ['_outputPinControlLabel', '_outputPinControl'],
            ['_enabledControl'],
            ['_iconControlLabel', '_iconControl'],
            ['_addLightBtn', '_cancelBtn']
        ]

        for l in layoutList:
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            panel.layout.setAlignment(Qt.AlignCenter)
            for ctrl in l:
                panel.layout.addWidget(eval('self.%s' % ctrl))
            self.layout.addWidget(panel)

    def __createLightBtnAction(self):
        self._light.name = self._nameControl.text()
        self._light.outputPin = int(self._outputPinControl.currentText())
        self._light.enabled = self._enabledControl.isChecked()
        self._light.icon = self._iconControl.currentData()
        if self.parent is not None:
            self.__closeTab()
            self.parent.createLight(self._light)

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
