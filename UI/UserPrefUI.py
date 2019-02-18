"""
=========================
TacOS User Preferences UI
=========================

The user preferences UI for the TacOS environment.  Allows setting of persistent UI configurations.

"""

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlButton
from pyforms.controls import ControlLabel
from pyforms.controls import ControlCombo
from pyforms.controls import ControlText
from Objects.Logger import Logger
from pyforms_gui.basewidget import no_columns


class UserPrefUI(BaseWidget):

    def __init__(self, prefs):
        BaseWidget.__init__(self, 'User Preferences')

        # Permanent controls
        self._logger = Logger('userPrefsUI', 'UI : User Preferences')
        self._closeBtn = ControlButton('Close')
        self._startMaximized = ControlCheckBox('Start Maximized')
        self._allowDuplicatePins = ControlCheckBox('Allow Duplicate Output Pins')
        self._enableOBA = ControlCheckBox('OnBoard Air')
        self._enableLighting = ControlCheckBox('Lighting')
        self._enableTracControl = ControlCheckBox('Traction Control')
        self._panelLabel = ControlLabel(
            '<html><center>Enable Modules:<br>\
            <em>Restart TacOS for changes to take effect.</em></center></html>'
        )
        self._i2cBus = ControlCombo('I2C Bus')
        self._i2cAddress = ControlText('I2C Address')
        self._i2cLabel = ControlLabel(
            '<html><center>I2C Parameters:<br>\
            <em>Restart TacOS for changes to take effect.</em></center></html>'
        )
        self._i2cDebug = ControlCheckBox('I2C Debug Mode')
        self._i2cDebugLabel = ControlLabel(
            '<html><center>I2C Debug Mode:<br>\
            <em>Disables all I2C comms.<br>\
            Restart TacOS for changes to take effect.</em></center></html>'
        )
        # Assign control properties
        for i in [0, 1]:
            self._i2cBus.add_item(str(i), i)
        _availablePrefs = prefs.keys()
        _prefKeys = ['startMaximized', 'allowDuplicatePins',
                     'enableOBA', 'enableLighting', 'enableTracControl',
                     'i2cBus', 'i2cAddress', 'i2cDebug']
        _defaultTrueKeys = ['enableOBA', 'enableLighting', 'enableTracControl']
        for key in _prefKeys:
            if key in _availablePrefs:
                exec("self._%s.value = prefs[key]" % key)
            elif key in _defaultTrueKeys:
                exec("self._%s.value = True" % key)
        if 'i2cBus' not in _availablePrefs:
            self._i2cBus.value = 1
        if 'i2cAddress' not in _availablePrefs:
            self._i2cAddress.value = '0x20'

        # Assign button functions
        self._closeBtn.value = self.__close

        # Assign form layout
        self._formset = [
            (' ', '_startMaximized', ' '),
            (' ', '_allowDuplicatePins', ' '),
            no_columns('_panelLabel'),
            ('_enableOBA', '_enableLighting', '_enableTracControl'),
            no_columns('_i2cLabel'),
            no_columns('_i2cBus', '_i2cAddress'),
            no_columns('_i2cDebugLabel'),
            (' ', '_i2cDebug', ' '),
            ' ',
            no_columns('_closeBtn')
        ]

    def __close(self):
        if self.parent is not None:
            self.parent.prefs = self.__getPrefs()
            self.parent.closePrefs()
        self.close()

    def __getPrefs(self):
        """
        Get preferences from UI form.
        :return: User preferences to store.
        :rtype: dict
        """
        return {
            'startMaximized': self._startMaximized.value,
            'allowDuplicatePins': self._allowDuplicatePins.value,
            'enableOBA': self._enableOBA.value,
            'enableLighting': self._enableLighting.value,
            'enableTracControl': self._enableTracControl.value,
            'i2cBus': self._i2cBus.value,
            'i2cAddress': hex(int(self._i2cAddress.value, 16)),
            'i2cDebug': self._i2cDebug.value
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


if __name__ == '__main__':
    pyforms.start_app(UserPrefUI)
