"""
=============
TacOS Main UI
=============

The main UI for the TacOS environment.  Envelops all other window modules in a docked frame.

"""

import os
import subprocess
import pickle

from AnyQt.QtCore import Qt
from AnyQt.QtGui import QIcon
from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLabel, QFrame, QScrollArea

from Objects import Config
from Objects.MenuButton import MenuButton
from Objects.CamViewer import CamViewer
from Objects.I2CBus import I2CBus
from Objects.Logger import Logger
from UI.LightConfigUI import LightConfigUI
from UI.LightControlUI import LightControlUI
from UI.OBAConfigUI import OBAConfigUI
from UI.OBAControlUI import OBAControlUI
from UI.TracConfigUI import TracConfigUI
from UI.TracControlUI import TracControlUI
from UI.UserPrefUI import UserPrefUI
from UI.Gyro import Gyrometer


class MainUI(QWidget):

    def __init__(self):
        super(MainUI, self).__init__()
        self.left = Config.geometry[0]
        self.top = Config.geometry[1]
        self.width = Config.geometry[2]
        self.height = Config.geometry[3]
        self.layout = QHBoxLayout(self)

        # Init logger
        self._logger = Logger('mainUI', 'UI : Main')

        # Read in user prefs
        self._prefs = {}
        self.__loadPrefs()

        # Init I2C control
        if 'i2cAddress' in self._prefs.keys():
            address = self._prefs['i2cAddress']
        else:
            address = '0x20'
        if 'i2cBus' in self._prefs.keys():
            bus = self._prefs['i2cBus']
        else:
            bus = 1
        if 'i2cDebug' in self._prefs.keys():
            debug = self._prefs['i2cDebug']
        else:
            debug = False
        self._i2cBus = I2CBus(int(bus), str(address), debug)
        del bus, address, debug

        # Create menu frame
        self._sidebarMenu = QFrame(self)
        self._sidebarMenu.layout = QVBoxLayout(self._sidebarMenu)
        self._sidebarMenu.setMaximumWidth(Config.menuWidth + 50)
        self._sidebarMenu.setMaximumHeight(Config.geometry[3])
        self._sidebarMenu.setStyleSheet("QFrame{border-right: 1px solid black}")

        # Create menu
        container = QWidget()
        container.layout = QVBoxLayout()
        container.setLayout(container.layout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(container)
        scrollArea.setWidgetResizable(True)
        self._sidebarMenu.layout.addWidget(scrollArea)
        for key in ['enableOBA', 'enableLighting', 'enableTracControl', 'enableCamViewer', 'enableGyro']:
            if key not in self._prefs.keys() or self._prefs[key]:
                title = {'enableOBA': 'Air',
                         'enableLighting': 'Lighting',
                         'enableTracControl': 'Traction',
                         'enableCamViewer': 'Camera',
                         'enableGyro': 'Gyro'}[key]
                icon = {'enableOBA': Config.faIcon("wind"),
                        'enableLighting': Config.faIcon("lightbulb"),
                        'enableTracControl': Config.icon("tracControl", "rearDiff")['path'],
                        'enableCamViewer': Config.faIcon("camera"),
                        'enableGyro': Config.faIcon("truck-pickup")}[key]
                button = MenuButton(panel=title, parent=self)
                button.setIcon(QIcon(icon))
                container.layout.addWidget(button)
        settingsButton = MenuButton(panel="Settings", parent=self)
        settingsButton.setIcon(QIcon(Config.faIcon("user-cog")))
        container.layout.addWidget(settingsButton)

        # Create version info label
        self._versionInfo = QLabel('v%s' % Config.version, self)
        self._versionInfo.setAlignment(Qt.AlignCenter)
        self._versionInfo.setFixedWidth(Config.menuWidth)
        self._versionInfo.setStyleSheet("QLabel{border: none}")
        self._sidebarMenu.layout.addWidget(self._versionInfo)

        # Create OSK button
        self._oskShow = QPushButton('', self)
        self._oskShow.setIcon(QIcon(Config.faIcon('keyboard')))
        self._oskShow.setFixedWidth(Config.menuWidth)
        self._oskShow.clicked.connect(self.__showOSK)
        self._sidebarMenu.layout.addWidget(self._oskShow)

        # Add menu frame to main UI
        self.layout.addWidget(self._sidebarMenu)

        # Create main UI panel
        self._UIPanel = QWidget(self)
        self._UIPanel.layout = QVBoxLayout(self._UIPanel)
        self.layout.addWidget(self._UIPanel)

        # Init control UIs
        self._UserPrefUI = UserPrefUI(self._prefs, parent=self)
        self._UserPrefUI.setParent(self)
        self._LightControlUI = LightControlUI(parent=self)
        self._LightControlUI.setParent(self)
        self._OBAControlUI = OBAControlUI(parent=self)
        self._OBAControlUI.setParent(self)
        self._TracControlUI = TracControlUI(parent=self)
        self._TracControlUI.setParent(self)
        try:
            self._CamViewer = CamViewer(0)
            self._CamViewer.setParent(self)
        except Exception as e:
            self._CamViewer = QWidget(self)
        self._Gyro = Gyrometer(parent=self)

        # Init config UIs
        self._LightConfigUI = LightConfigUI(parent=self)
        self._OBAConfigUI = OBAConfigUI(parent=self)
        self._TracConfigUI = TracConfigUI(parent=self)

        # UI map
        self.UIMap = {
            "Air": self._OBAControlUI,
            "Lighting": self._LightControlUI,
            "Traction": self._TracControlUI,
            "Camera": self._CamViewer,
            "Gyro": self._Gyro,
            "Settings": self._UserPrefUI
        }

        # Control UI map
        self.ConfigUIMap = {
            "Air": self._OBAConfigUI,
            "Lighting": self._LightConfigUI,
            "Traction": self._TracConfigUI
        }

        # Add UIs to main panel and hide
        for obj in [self._OBAControlUI, self._TracControlUI, self._LightControlUI,
                    self._CamViewer, self._UserPrefUI, self._Gyro,
                    self._OBAConfigUI, self._LightConfigUI, self._TracConfigUI]:
            self._UIPanel.layout.addWidget(obj)
            obj.hide()

        # Create button panel
        self._btnPanel = QWidget(self)
        self._btnPanel.layout = QHBoxLayout(self._btnPanel)
        self._UIPanel.layout.addWidget(self._btnPanel)

        # Create Config button
        self._configBtn = QPushButton('Configure', self)
        self._configBtn.setFixedHeight(50)
        self._configBtn.setIcon(QIcon(Config.faIcon('cog')))
        self._configBtn.clicked.connect(self.__configBtnAction)
        self._btnPanel.layout.addWidget(self._configBtn)

        # Set initial UI
        for key in ['enableOBA', 'enableLighting', 'enableTracControl', 'enableCamViewer']:
            if key in self._prefs.keys():
                if self._prefs[key]:
                    panel = {'enableOBA': self._OBAControlUI,
                             'enableLighting': self._LightControlUI,
                             'enableTracControl': self._TracControlUI,
                             'enableCamViewer': self._CamViewer}[key]
                    panel.show()
                    break

        # Create Night Mode button
        self._nightMode = QPushButton('', self)
        self._nightMode.setFixedHeight(50)
        try:
            icon = {True: Config.faIcon('sun'), False: Config.faIcon('moon')}[self._prefs['nightMode']]
            self._nightMode.setIcon(QIcon(icon))
        except KeyError:
            self._nightMode.setIcon(QIcon(Config.faIcon('sun')))
        try:
            text = {True: 'Day Mode', False: 'Night Mode'}[self._prefs['nightMode']]
            self._nightMode.setText(text)
        except KeyError:
            self._nightMode.setText('Day Mode')
        self._nightMode.clicked.connect(self.__nightModeBtnAction)
        self._btnPanel.layout.addWidget(self._nightMode)
        self.setNightMode(self._prefs['nightMode'])

    def setUIPanel(self, panel):
        for key, value in self.ConfigUIMap.items():
            value.hide()
        for key, value in self.UIMap.items():
            value.hide()
        self.UIMap[panel].show()
        if panel == "Camera":
            self._CamViewer.start()
        else:
            self._CamViewer.stop()
        if panel == "Gyro":
            self._Gyro.startSerial()
            self._Gyro.startRotation()
        else:
            self._Gyro.stopSerial()
            self._Gyro.stopRotation()

    def refreshConfigPanels(self):
        self._OBAConfigUI = OBAConfigUI(parent=self)
        self._LightConfigUI = LightConfigUI(parent=self)
        self._TracConfigUI = TracConfigUI(parent=self)

    def showConfigPanel(self):
        self.refreshConfigPanels()
        self.disableConfigButtons()
        self.configBtn.hide()
        for ui in [self._TracConfigUI, self._OBAConfigUI, self._LightConfigUI]:
            ui.hide()
        self.ConfigUIMap[self.currentUIPanel()].show()

    def currentUIPanel(self):
        for key, value in self.UIMap.items():
            if value.isVisible():
                return key

    def closeEvent(self, event):
        self.__savePrefs()
        self._i2cBus.deEnergizeAll()

    def closePrefs(self):
        self.__savePrefs()
        self.redrawTracPanel(self._TracControlUI.tracs, False)
        self.redrawLightPanel(self._LightControlUI.lights, False)
        self.redrawOBAPanel(self._OBAControlUI.obas, False)

    def closeConfig(self, config, obj):
        if config == "Lighting":
            self.redrawLightPanel(obj, False)
        elif config == "Air:":
            self.redrawOBAPanel(obj, False)
        elif config == "Traction":
            self.redrawTracPanel(obj, False)
        for configUI in self.ConfigUIMap.values():
            configUI.hide()
        self.UIMap[config].show()
        self.configBtn.show()
        self.enableConfigButtons()

    def redrawLightPanel(self, lights, setWin=False):
        self._LightControlUI = LightControlUI(parent=self)
        self._LightControlUI.setParent(self)
        if setWin:
            self.setUIPanel("Lighting")
            self.enableConfigButtons()
        # if not setWin:
        #     self.disableConfigButtons()
        for key in lights:
            if lights[key]['active']:
                control = eval('self._LightControlUI._%s' % key)
                control.setChecked(True)

    def redrawOBAPanel(self, obas, setWin=False):
        self._OBAControlUI = OBAControlUI(parent=self)
        self._OBAControlUI.setParent(self)
        if setWin:
            self.setUIPanel("Air")
            self.enableConfigButtons()
        # if not setWin:
        #     self.disableConfigButtons()
        for key in obas:
            if obas[key]['active']:
                control = eval('self._OBAControlUI._%s' % key)
                control.setChecked(True)

    def redrawTracPanel(self, tracs, setWin=False):
        self._TracControlUI = TracControlUI(parent=self)
        self._TracControlUI.setParent(self)
        if setWin:
            self.setUIPanel("Traction")
            self.enableConfigButtons()
        # if not setWin:
        #     self.disableConfigButtons()
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
        for control in [self._configBtn]:
            control.setEnabled(False)

    def enableConfigButtons(self):
        for control in [self._configBtn]:
            control.setEnabled(True)

    def setNightMode(self, mode):
        """
        Set the display brightness mode.
        :param mode: The display mode to set (True for day, False for night)
        :type mode: bool
        :return: None
        """
        _value = {False: Config.dayBright, True: Config.nightBright}[mode]
        self._nightMode.setIcon({True: QIcon(Config.faIcon('sun')),
                                 False: QIcon(Config.faIcon('moon'))}
                                [mode])
        self._nightMode.setText({True: 'Day Mode', False: 'Night Mode'}[mode])
        _cmd = "echo %s > /sys/class/backlight/rpi_backlight/brightness" % _value
        _subProc = subprocess.run(_cmd, shell=True)
        if _subProc.returncode != 0:
            self.logger.log('Failed to set night mode: %s' % _subProc.stderr)

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
        currentUI = self.currentUIPanel()
        if currentUI not in ['Camera', 'Gyro']:
            self.disableConfigButtons()
            # Hide UI
            self.UIMap[currentUI].hide()
            # Show config UI
            self.ConfigUIMap[currentUI].show()
            self._configBtn.setVisible(False)

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
    def UIPanel(self):
        return self._UIPanel

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
