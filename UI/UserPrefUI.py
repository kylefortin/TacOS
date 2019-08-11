"""
=========================
TacOS User Preferences UI
=========================

The user preferences UI for the TacOS environment.  Allows setting of persistent UI configurations.

"""

import pyforms
from AnyQt.QtWidgets import QWidget
from AnyQt.QtWidgets import QCheckBox, QPushButton
from AnyQt.QtWidgets import QLabel, QComboBox
from AnyQt.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout
from AnyQt.QtCore import Qt
from Objects.Logger import Logger
from Objects import Config


class UserPrefUI(QWidget):

    def __init__(self, prefs, parent=None):
        super(UserPrefUI, self).__init__()
        self.title = 'User Preferences'
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._parent = parent

        # Permanent controls
        self._logger = Logger('userPrefsUI', 'UI : User Preferences')
        self._closeBtn = QPushButton('Close', self)
        self._closeBtn.clicked.connect(self.__close)
        self._startMaximized = QCheckBox('Start Maximized', self)
        self._allowDuplicatePins = QCheckBox('Allow Duplicate Output Pins', self)
        self._enableOBA = QCheckBox('OnBoard Air', self)
        self._enableLighting = QCheckBox('Lighting', self)
        self._enableTracControl = QCheckBox('Traction Control', self)
        self._enableCamViewer = QCheckBox('Camera Viewer', self)
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

        # Set initial values
        for control in ['startMaximized', 'allowDuplicatePins', 'enableOBA',
                        'enableLighting', 'enableTracControl', 'enableCamViewer', 'i2cDebug', 'debugLogging']:
            if control in prefs.keys():
                exec('self._%s.setChecked(prefs["%s"])' % (control, control))
            else:
                if control in ['enableOBA', 'enableLighting', 'enableTracControl', 'enableCamViewer']:
                    exec('self._%s.setChecked(True)' % control)
                else:
                    exec('self._%s.setChecked(False)' % control)
        if 'i2cAddress' in prefs.keys():
            self._i2cAddress.setText(prefs['i2cAddress'])
        else:
            self._i2cAddress.setText('0x20')
        if 'i2cBus' in prefs.keys():
            self._i2cBus.setCurrentText(str(prefs['i2cBus']))
        else:
            self._i2cBus.setCurrentIndex(0)

        layoutList = [
            ['_startMaximized', '_allowDuplicatePins', '_debugLogging'],
            ['_panelLabel'],
            ['_enableOBA', '_enableLighting', '_enableTracControl', '_enableCamViewer'],
            ['_i2cLabel'],
            ['_i2cBusLabel', '_i2cBus', '_i2cAddress'],
            ['_i2cDebugLabel'],
            ['_i2cDebug'],
            ['_closeBtn']
        ]
        for i in layoutList:
            panel = QWidget()
            panel.layout = QHBoxLayout(panel)
            panel.layout.setAlignment(Qt.AlignCenter)
            for c in i:
                panel.layout.addWidget(eval('self.%s' % c))
            self.layout.addWidget(panel)

    def refresh(self):
        self.__init__(self.window().prefs, self._parent)

    def __close(self):
        if self._parent is not None:
            self._parent.prefs = self.__getPrefs()
            self._parent.closePrefs()

    def __getPrefs(self):
        """
        Get preferences from UI form.
        :return: User preferences to store.
        :rtype: dict
        """
        return {
            'startMaximized': self._startMaximized.isChecked(),
            'allowDuplicatePins': self._allowDuplicatePins.isChecked(),
            'enableOBA': self._enableOBA.isChecked(),
            'enableLighting': self._enableLighting.isChecked(),
            'enableTracControl': self._enableTracControl.isChecked(),
            'i2cBus': self._i2cBus.currentText(),
            'i2cAddress': hex(int(self._i2cAddress.text(), 16)),
            'i2cDebug': self._i2cDebug.isChecked(),
            'debugLogging': self._debugLogging.isChecked(),
            'enableCamViewer': self._enableCamViewer.isChecked()
        }

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, name='', title=''):
        """
        Set the internal logger name and title
        :param name: The backend name of the logger.
        :type name: str
        :param title: The display title of the logger.
        :type title: str
        :return: None
        """
        if name != '':
            self._logger.name = name
        if title != '':
            self._logger.title = title
