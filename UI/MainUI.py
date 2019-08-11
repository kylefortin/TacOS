"""
=============
TacOS Main UI
=============

The main UI for the TacOS environment.  Envelops all other window modules in a docked frame.

"""

import pickle
import sys
import os
from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QTabWidget, QPushButton, QLabel
from AnyQt.QtGui import QIcon
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.I2CBus import I2CBus
from Objects.CamViewer import CamViewer
from Objects.Logger import Logger
from UI.LightControlUI import LightControlUI
from UI.LightConfigUI import LightConfigUI
from UI.OBAControlUI import OBAControlUI
from UI.OBAConfigUI import OBAConfigUI
from UI.TracControlUI import TracControlUI
from UI.TracConfigUI import TracConfigUI
from UI.UserPrefUI import UserPrefUI


class MainUI(QWidget):

    def __init__(self):
        super(MainUI, self).__init__()
        self.left = Config.geometry[0]
        self.top = Config.geometry[1]
        self.width = Config.geometry[2]
        self.height = Config.geometry[3]
        self.layout = QVBoxLayout(self)

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
        self._LightControlUI = LightControlUI(parent=self)
        self._LightControlUI.setParent(self)
        self._OBAControlUI = OBAControlUI(parent=self)
        self._OBAControlUI.setParent(self)
        self._TracControlUI = TracControlUI(parent=self)
        self._TracControlUI.setParent(self)
        self._CamViewer = CamViewer(0)
        self._CamViewer.setParent(self)

        # Create tab strip
        self._tabs = QTabWidget(self)
        for key in ['enableOBA', 'enableLighting', 'enableTracControl', 'enableCamViewer']:
            if key not in self._prefs.keys() or self._prefs[key]:
                title = {'enableOBA': 'OnBoard Air',
                         'enableLighting': 'Lighting',
                         'enableTracControl': 'Traction Control',
                         'enableCamViewer': 'Camera Viewer'}[key]
                panel = {'enableOBA': '_OBAControlUI',
                         'enableLighting': '_LightControlUI',
                         'enableTracControl': '_TracControlUI',
                         'enableCamViewer': '_CamViewer'}[key]
                self._tabs.addTab(eval('self.%s' % panel), title)
        self._tabs.currentChanged.connect(self.__tabChange)
        self.layout.addWidget(self._tabs)

        # Create button panel
        self._btnPanel = QWidget(self)
        self._btnPanel.layout = QHBoxLayout(self._btnPanel)
        self.layout.addWidget(self._btnPanel)

        # Create Config button
        self._configBtn = QPushButton('', self)
        self._configBtn.setFixedHeight(50)
        self._configBtn.setIcon(QIcon(Config.faIcon('cog')))
        self._configBtn.clicked.connect(self.__configBtnAction)
        self._btnPanel.layout.addWidget(self._configBtn)

        # Create User Prefs button
        self._settingsBtn = QPushButton('User Prefs', self)
        self._settingsBtn.setIcon(QIcon(Config.faIcon('user-cog')))
        self._settingsBtn.setFixedHeight(50)
        self._settingsBtn.clicked.connect(self.__settingsBtnAction)
        self._btnPanel.layout.addWidget(self._settingsBtn)

        # Create Night Mode button
        self._nightMode = QPushButton('', self)
        self._nightMode.setFixedHeight(50)
        try:
            self._nightMode.setIcon(QIcon({True: Config.faIcon('sun'), False: Config.faIcon('moon')}\
                [self._prefs['nightMode']]))
        except KeyError:
            self._nightMode.setIcon(QIcon(Config.faIcon('sun')))
        try:
            self._nightMode.setText({True: 'Day Mode', False: 'Night Mode'}[self._prefs['nightMode']])
        except KeyError:
            self._nightMode.setText('Day Mode')
        self._nightMode.clicked.connect(self.__nightModeBtnAction)
        self._btnPanel.layout.addWidget(self._nightMode)

        bottomPanel = QWidget(self)
        bottomPanel.layout = QHBoxLayout(bottomPanel)
        bottomPanel.layout.addWidget(QWidget(self))
        # Create version info label
        self._versionInfo = QLabel('v%s' % Config.version, self)
        bottomPanel.layout.addWidget(self._versionInfo)
        bottomPanel.layout.setAlignment(Qt.AlignCenter)
        # Create OSK button
        self._oskShow = QPushButton('', self)
        self._oskShow.setIcon(QIcon(Config.faIcon('keyboard')))
        self._oskShow.setFixedWidth(100)
        self._oskShow.clicked.connect(self.__showOSK)
        bottomPanel.layout.addWidget(self._oskShow)
        self.layout.addWidget(bottomPanel)

    def __tabChange(self):
        if 'Camera Viewer' in self.tabs.tabText(self.tabs.currentIndex()):
            self._CamViewer.start()
        else:
            self._CamViewer.stop()

    def setConfigLabel(self):
        self._configBtn.setText('Configure ' + self._tabs.tabText(self._tabs.currentIndex()))

    def closeEvent(self, event):
        self.__savePrefs()
        self._i2cBus.deEnergizeAll()

    def closePrefs(self):
        for i in range(self.tabs.count()):
            if 'User Prefs' in self.tabs.tabText(i):
                self.tabs.removeTab(i)
        self.redrawTracPanel(self._TracControlUI.tracs, False)
        self.redrawLightPanel(self._LightControlUI.lights, False)
        self.redrawOBAPanel(self._OBAControlUI.obas, True)
        self.__savePrefs()

    def showEvent(self, event):
        self.setConfigLabel()

    def paintEvent(self, event):
        self.setConfigLabel()

    def redrawLightPanel(self, lights, setWin=False):
        self._LightControlUI = LightControlUI(parent=self)
        self._LightControlUI.setParent(self)
        for i in range(self._tabs.count()):
            self._tabs.setTabEnabled(i, True)
            if 'Lighting' in self._tabs.tabText(i):
                self._tabs.removeTab(i)
                if i >= self._tabs.count():
                    self._tabs.addTab(self._LightControlUI, 'Lighting')
                else:
                    self._tabs.insertTab(i, self._LightControlUI, 'Lighting')
                if setWin:
                    self._tabs.setCurrentIndex(i)
                    self.enableConfigButtons()
        if not setWin:
            self.disableConfigButtons()
        for key in lights:
            if lights[key]['active']:
                control = eval('self._LightControlUI._%s' % key)
                control.setChecked(True)

    def redrawOBAPanel(self, obas, setWin=False):
        self._OBAControlUI = OBAControlUI(parent=self)
        self._OBAControlUI.setParent(self)
        for i in range(self._tabs.count()):
            self._tabs.setTabEnabled(i, True)
            if 'OnBoard Air' in self._tabs.tabText(i):
                self._tabs.removeTab(i)
                if i >= self._tabs.count():
                    self._tabs.addTab(self._OBAControlUI, 'OnBoard Air')
                else:
                    self._tabs.insertTab(i, self._OBAControlUI, 'OnBoard Air')
                if setWin:
                    self._tabs.setCurrentIndex(i)
                    self.enableConfigButtons()
        if not setWin:
            self.disableConfigButtons()
        for key in obas:
            if obas[key]['active']:
                control = eval('self._OBAControlUI._%s' % key)
                control.setChecked(True)

    def redrawTracPanel(self, tracs, setWin=False):
        self._TracControlUI = TracControlUI(parent=self)
        self._TracControlUI.setParent(self)
        for i in range(self._tabs.count()):
            self._tabs.setTabEnabled(i, True)
            if 'Traction Control' in self._tabs.tabText(i):
                self._tabs.removeTab(i)
                if i >= self._tabs.count():
                    self._tabs.addTab(self._TracControlUI, 'Traction Control')
                else:
                    self._tabs.insertTab(i, self._TracControlUI, 'Traction Control')
                if setWin:
                    self._tabs.setCurrentIndex(i)
                    self.enableConfigButtons()
        if not setWin:
            self.disableConfigButtons()
        for key in tracs:
            if tracs[key]['active']:
                control = eval('self._TracControlUI._%s' % key)
                control.setChecked(True)

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
            control.setEnabled(False)

    def enableConfigButtons(self):
        for control in [self._settingsBtn, self._configBtn]:
            control.setEnabled(True)

    def toggleNightMode(self):
        try:
            _currentMode = self.prefs['nightMode']
        except KeyError:
            _currentMode = False
        _value = {True: Config.dayBright, False: Config.nightBright}[_currentMode]
        self._nightMode.setIcon({True: QIcon(Config.faIcon('sun')),
                                 False: QIcon(Config.faIcon('moon'))}
                                [not _currentMode])
        self._nightMode.setText({True: 'Day Mode', False: 'Night Mode'}[not _currentMode])
        _cmd = "echo %s > /sys/class/backlight/rpi_backlight/brightness" % _value
        os.system(_cmd)
        self.prefs['nightMode'] = not _currentMode
        self.__savePrefs()
        self.logger.log('Night mode %s: backlight set to %s' % (not _currentMode, _value))

    def __savePrefs(self):
        pPrefs = open(Config.prefs, 'wb')
        pickle.dump(self._prefs, pPrefs)
        pPrefs.close()

    def __loadPrefs(self):
        pPrefs = open(Config.prefs, 'rb')
        _prefs = pickle.load(pPrefs)
        for key in _prefs:
            self._prefs[key] = _prefs[key]
        pPrefs.close()

    def __configBtnAction(self):
        tab = self._tabs.tabText(self._tabs.currentIndex())
        self.disableConfigButtons()
        if 'OnBoard Air' in tab:
            ui = OBAConfigUI(parent=self)
        elif 'Lighting' in tab:
            ui = LightConfigUI(parent=self)
        else:
            ui = TracConfigUI(parent=self)
        ui.setParent(self)
        # Disable other tabs
        for i in range(self.tabs.count()):
            self.tabs.setTabEnabled(i, False)
        i = self._tabs.addTab(ui, 'Configure %s' % tab)
        self._tabs.setCurrentIndex(i)
        self._configBtn.setVisible(False)

    def __settingsBtnAction(self):
        self.disableConfigButtons()
        self._PrefsUI = UserPrefUI(self._prefs, parent=self)
        self._PrefsUI.setParent(self)
        idx = self._tabs.addTab(self._PrefsUI, 'User Prefs')
        self._tabs.setCurrentIndex(idx)
        for i in range(self._tabs.count()):
            if self._tabs.tabText(i) in ['OnBoard Air', 'Lighting', 'Traction Control']:
                self._tabs.setTabEnabled(i, False)

    def __nightModeBtnAction(self):
        self.toggleNightMode()

    def __showOSK(self):
        if self.window().dock.isHidden():
            self.window().dock.show()
        else:
            self.window().dock.hide()

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
    def lightDisplayWidget(self):
        return self._lightDisplayWidget

    @property
    def obaDisplayWidget(self):
        return self._obaDisplayWidget

    @property
    def tracDisplayWidget(self):
        return self._tracDisplayWidget

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

    @property
    def tabs(self):
        return self._tabs
