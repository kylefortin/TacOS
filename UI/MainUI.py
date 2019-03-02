"""
=============
TacOS Main UI
=============

The main UI for the TacOS environment.  Envelops all other window modules in a docked frame.

"""

import pickle

import sys

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlEmptyWidget
from pyforms.controls import ControlLabel

from pyforms_gui.basewidget import no_columns

from AnyQt.QtWidgets import QTabWidget

from Objects import Config
from Objects.I2CBus import I2CBus
from Objects.Logger import Logger
from UI.LightControlUI import LightControlUI
from UI.OBAControlUI import OBAControlUI
from UI.TracControlUI import TracControlUI
from UI.UserPrefUI import UserPrefUI


class MainUI(BaseWidget):

    def __init__(self):

        BaseWidget.__init__(self, 'TacOS')

        # Init logger
        self._logger = Logger('mainUI', 'UI : Main')

        # Read in user prefs
        self._prefs = {}
        self.__loadPrefs()

        # Init I2C control
        if 'i2cAddress' in self._prefs.keys():
            address = self._prefs['i2cAddress']
        else:
            address = 0x20
        if 'i2cBus' in self._prefs.keys():
            bus = self._prefs['i2cBus']
        else:
            bus = 1
        if 'i2cDebug' in self._prefs.keys():
            debug = self._prefs['i2cDebug']
        else:
            debug = False
        self._i2cBus = I2CBus(bus, address, debug)
        del bus, address, debug

        # Init control UIs
        self._LightControlUI = LightControlUI()
        self._LightControlUI.parent = self
        self._lightPanel = ControlEmptyWidget()
        self._OBAControlUI = OBAControlUI()
        self._OBAControlUI.parent = self
        self._obaPanel = ControlEmptyWidget()
        self._TracControlUI = TracControlUI()
        self._TracControlUI.parent = self
        self._tracPanel = ControlEmptyWidget()
        self._configBtn = ControlButton()
        self._settingsBtn = ControlButton('User Prefs')
        self._versionInfo = ControlLabel('v%s' % Config.version)

        # Assign control properties
        self._tracPanel.value = self._TracControlUI
        self._lightPanel.value = self._LightControlUI
        self._obaPanel.value = self._OBAControlUI
        self._configBtn.icon = Config.faIcon('cog')
        self._configBtn._form.setFixedHeight(50)
        self._settingsBtn.icon = Config.faIcon('user-cog')
        self._settingsBtn._form.setFixedHeight(50)

        # Assign button functions
        self._configBtn.value = self.__configBtnAction
        self._settingsBtn.value = self.__settingsBtnAction

        # Assign form layout
        i = ord('a')
        formset = "self._formset = [no_columns({"
        for key in ['enableOBA', 'enableLighting', 'enableTracControl']:
            if key not in self._prefs.keys() or self._prefs[key]:
                letter = eval({True: 'unichr(i)', False: 'chr(i)'}[sys.version_info[0] < 3])
                title = {'enableOBA': 'OnBoard Air',
                         'enableLighting': 'Lighting',
                         'enableTracControl': 'Traction Control'}[key]
                panel = {'enableOBA': '_obaPanel',
                         'enableLighting': '_lightPanel',
                         'enableTracControl': '_tracPanel'}[key]
                formset += "'%s:%s': ['%s']," % (letter, title, panel)
                i += 1
        formset = formset[:-1] + "}), ('_configBtn', '_settingsBtn'), ('_versionInfo')]"
        exec(formset)
        del formset

    def setConfigLabel(self):
        self._configBtn.label = 'Configure ' + self._tabs[0].tabText(self._tabs[0].currentIndex())

    def closeEvent(self, event):
        self.__savePrefs()
        self._i2cBus.deEnergizeAll()

    def closePrefs(self):
        self.redrawLightPanel(self._LightControlUI.lights, True)
        self.redrawOBAPanel(self._OBAControlUI.obas, True)
        self.redrawTracPanel(self._TracControlUI.tracs, True)
        self.enableConfigButtons()

    def showEvent(self, event):
        self.setConfigLabel()

    def paintEvent(self, event):
        self.setConfigLabel()

    def redrawLightPanel(self, lights, setWin=False):
        self._LightControlUI = LightControlUI()
        self._LightControlUI.parent = self
        if setWin:
            self.enableConfigButtons()
            self._lightPanel.value = self._LightControlUI
        else:
            self.disableConfigButtons()
        for key in lights:
            if lights[key]['active']:
                control = eval('self._LightControlUI._%s' % key)
                control.form.setChecked(True)

    def redrawOBAPanel(self, obas, setWin=False):
        self._OBAControlUI = OBAControlUI()
        self._OBAControlUI.parent = self
        if setWin:
            self.enableConfigButtons()
            self._obaPanel.value = self._OBAControlUI
        else:
            self.disableConfigButtons()
        for key in obas:
            if obas[key]['active']:
                control = eval('self._OBAControlUI._%s' % key)
                control.form.setChecked(True)

    def redrawTracPanel(self, tracs, setWin=False):
        self._TracControlUI = TracControlUI()
        self._TracControlUI.parent = self
        if setWin:
            self.enableConfigButtons()
            self._tracPanel.value = self._TracControlUI
        else:
            self.disableConfigButtons()
        for key in tracs:
            if tracs[key]['active']:
                control = eval('self._TracControlUI._%s' % key)
                control.form.setChecked(True)

    def availablePins(self, value=None):
        if not self._prefs['allowDuplicatePins']:
            pinsDict = {}
            i = 0
            for pin in Config.outputPinList:
                pinsDict[i] = pin
                i += 1
            usedPins = []
            for key in self._LightControlUI.lights.keys():
                usedPins.append(self._LightControlUI.lights[key]['outputPin'])
            for key in self._OBAControlUI.obas.keys():
                usedPins.append(self._OBAControlUI.obas[key]['outputPin'])
            for key in self._TracControlUI.tracs.keys():
                usedPins.append(self._TracControlUI.tracs[key]['outputPin'])
            for pin in usedPins:
                for key in pinsDict.keys():
                    if pinsDict[key] == pin:
                        pinsDict.pop(key)
                        break
            pins = []
            for key in pinsDict.keys():
                pins.append(int(pinsDict[key]))
            if value is not None:
                pins.append(int(value))
            del pinsDict
        else:
            pins = Config.outputPinList
        return next(x for x in (pins.sort(), pins) if x is not None)

    def setOutputPin(self, pin, state):
        """
        Set the given relay (pin) to the desired state).
        :param pin: The output pin to set state for.
        :type pin: int
        :param state: State to set the output pin to (T=high, F=low)
        :type state: bool
        :return: None
        """
        fx = {
            True: self._i2cBus.energizeRelay,
            False: self._i2cBus.deEnergizeRelay
        }[state]
        fx(pin)

    def disableConfigButtons(self):
        for control in [self._settingsBtn, self._configBtn]:
            control.enabled = False

    def enableConfigButtons(self):
        for control in [self._settingsBtn, self._configBtn]:
            control.enabled = True

    def __savePrefs(self):
        pPrefs = open(Config.prefs, 'wb')
        pickle.dump(self._prefs, pPrefs)
        pPrefs.close()

    def __loadPrefs(self):
        pPrefs = open(Config.prefs, 'rb')
        _prefs = pickle.load(pPrefs)
        for key in _prefs:
            self._prefs[key] = _prefs[key]
        if 'allowDuplicates' not in self._prefs.keys():
            self._prefs['allowDuplicates'] = False
        pPrefs.close()

    def __configBtnAction(self):
        tab = self._configBtn.label
        self.disableConfigButtons()
        if 'OnBoard Air' in tab:
            self._obaPanel.value.configBtnAction()
        elif 'Lighting' in tab:
            self._lightPanel.value.configBtnAction()
        else:
            self._tracPanel.value.configBtnAction()

    def __settingsBtnAction(self):
        tab = self._configBtn.label
        win = UserPrefUI(self._prefs)
        win.parent = self
        self.disableConfigButtons()
        if 'OnBoard Air' in tab:
            self._obaPanel.value = win
        elif 'Lighting' in tab:
            self._lightPanel.value = win
        else:
            self._tracPanel.value = win

    @property
    def LightControlUI(self):
        return self._LightControlUI

    @property
    def OBAControlUI(self):
        return self._OBAControlUI

    @property
    def TracControlUI(self):
        return self._TracControlUI

    @property
    def lightPanel(self):
        return self._lightPanel

    @property
    def obaPanel(self):
        return self._obaPanel

    @property
    def tracPanel(self):
        return self._tracPanel

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

    @property
    def prefs(self):
        return self._prefs

    @prefs.setter
    def prefs(self, value):
        """
        Set the global user preferences.
        :param value: Preferences to add or set.
        :type value: dict
        :return: None
        """
        if type(value) is not dict:
            raise TypeError(
                'Preferences value must be of type <dict>.  Supplied value is of type %s' % type(value)
            )
        elif len(value.keys()) == 0:
            raise ValueError(
                'Invalid preferences object. Object has len %s' % len(value.keys())
            )
        else:
            for key in value.keys():
                self._prefs[key] = value[key]

    @property
    def i2cBus(self):
        return self._i2cBus

    @property
    def configBtn(self):
        return self._configBtn


if __name__ == '__main__':
    pyforms.start_app(MainUI)
