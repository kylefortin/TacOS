"""
=========================
TacOS User Preferences UI
=========================

The user preferences UI for the TacOS environment.  Allows setting of persistent UI configurations.

"""

from AnyQt.QtWidgets import QWidget
from AnyQt.QtWidgets import QCheckBox, QPushButton
from AnyQt.QtWidgets import QLabel, QComboBox
from AnyQt.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QScrollArea, QGroupBox
from AnyQt.QtCore import Qt
from Objects.Logger import Logger
from Objects import Config
import sys
import os


class UserPrefUI(QWidget):

    def __init__(self, parent):
        super(UserPrefUI, self).__init__()
        self.title = 'User Preferences'
        self.setLayout(QVBoxLayout(self))
        self.parent = parent
        self.prefs = self.parent.prefs

        # Init logger
        self.logger = Logger('userPrefsUI', 'UI : User Preferences')

        # Set up container
        container = QWidget()
        container.setLayout(QVBoxLayout())

        # Set up scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidget(container)
        scrollArea.setWidgetResizable(True)
        self.layout().addWidget(scrollArea)

        # Permanent controls
        self._saveButton = QPushButton('Save', self)
        self._saveButton.clicked.connect(self.__save)
        self._startMaximized = QCheckBox('Start Maximized', self)
        self._allowDuplicatePins = QCheckBox('Allow Duplicate Output Pins', self)
        self._enableOBA = QCheckBox('OnBoard Air', self)
        self._enableLighting = QCheckBox('Lighting', self)
        self._enableTracControl = QCheckBox('Traction Control', self)
        self._enableCamViewer = QCheckBox('Camera Viewer', self)
        self._enableGyro = QCheckBox('Inclinometer', self)
        self._panelLabel = QLabel(
            '<html><center>Enable Modules:<br>\
            <em>Restart TacOS for changes to take effect.</em></center></html>', self
        )
        self._i2cBus = QComboBox(self)
        self._i2cBus.addItems(Config.busList)
        self._i2cBusLabel = QLabel('I2C Bus', self)
        self._i2cAddress = QLineEdit('I2C Address', self)
        self._i2cLabel = QLabel(
            '<html><center>I2C Parameters:<br>\
            <em>Restart TacOS for changes to take effect.</em></center></html>', self
        )
        self._i2cDebug = QCheckBox('I2C Debug Mode', self)
        self._i2cDebugLabel = QLabel(
            '<html><center>I2C Debug Mode:<br>\
            <em>Disables all I2C comms.<br>\
            Restart TacOS for changes to take effect.</em></center></html>', self
        )
        self._debugLogging = QCheckBox('Enable Debug Logs', self)
        self._restartButton = QPushButton('Restart TacOS', self)
        self._restartButton.clicked.connect(self.__restart)

        # Set initial values
        for control in ['startMaximized', 'allowDuplicatePins', 'enableOBA',
                        'enableLighting', 'enableTracControl', 'enableCamViewer', 'enableGyro',
                        'i2cDebug', 'debugLogging']:
            if control in self.prefs.keys():
                exec('self._%s.setChecked(self.prefs["%s"])' % (control, control))
            else:
                if control in ['enableOBA', 'enableLighting', 'enableTracControl',
                               'enableCamViewer', 'enableGyro']:
                    exec('self._%s.setChecked(True)' % control)
                else:
                    exec('self._%s.setChecked(False)' % control)
        if 'i2cAddress' in self.prefs.keys():
            self._i2cAddress.setText(self.prefs['i2cAddress'])
        else:
            self._i2cAddress.setText('0x20')
        if 'i2cBus' in self.prefs.keys():
            self._i2cBus.setCurrentText(str(self.prefs['i2cBus']))
        else:
            self._i2cBus.setCurrentIndex(0)

        layoutList = [
            ['_startMaximized', '_allowDuplicatePins', '_debugLogging'],
            ['_panelLabel'],
            ['_enableOBA', '_enableLighting', '_enableTracControl'],
            ['_enableCamViewer', '_enableGyro'],
            ['_i2cLabel'],
            ['_i2cBusLabel', '_i2cBus', '_i2cAddress'],
            ['_i2cDebugLabel'],
            ['_i2cDebug'],
            ['_saveButton', '_restartButton']
        ]
        for i in layoutList:
            panel = QWidget()
            panel.setLayout(QHBoxLayout(panel))
            panel.layout().setSpacing(20)
            panel.layout().setAlignment(Qt.AlignCenter)
            for c in i:
                panel.layout().addWidget(eval('self.%s' % c))
            container.layout().addWidget(panel)

    def refresh(self):
        self.__init__(self.window().prefs, self.parent)

    def __save(self):
        _prefs = self.__getPrefs()
        self.parent.prefs = _prefs
        Config.setPrefs(_prefs)

    def __restart(self):
        os.system("sudo sh /home/pi/TacOS/launcher.sh")
        sys.exit()

    def __getPrefs(self):
        _updates = {
            'startMaximized': self._startMaximized.isChecked(),
            'allowDuplicatePins': self._allowDuplicatePins.isChecked(),
            'enableOBA': self._enableOBA.isChecked(),
            'enableLighting': self._enableLighting.isChecked(),
            'enableTracControl': self._enableTracControl.isChecked(),
            'enableCamViewer': self._enableCamViewer.isChecked(),
            'enableGyro': self._enableGyro.isChecked(),
            'i2cBus': self._i2cBus.currentText(),
            'i2cAddress': hex(int(self._i2cAddress.text(), 16)),
            'i2cDebug': self._i2cDebug.isChecked(),
            'debugLogging': self._debugLogging.isChecked()
        }
        for _ in _updates.keys():
            self.prefs[_] = _updates[_]
        return self.prefs

