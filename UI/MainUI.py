"""
=============
TacOS Main UI
=============

The main UI for the TacOS environment.  Envelops all other window modules in a docked frame.

"""

import os, pickle

from AnyQt.QtCore import Qt
from AnyQt.QtGui import QIcon
from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLabel, QFrame, QScrollArea
from Objects import Config
from Objects.Lights import Lights
from Objects.OBAs import OBAs
from Objects.Tracs import Tracs
from Objects.MenuButton import MenuButton
from Objects.CamViewer import CamViewer
from Objects.I2CBus import I2CBus
from Objects.Logger import Logger
from UI.AddLightUI import AddLightUI
from UI.EditLightUI import EditLightUI
from UI.LightConfigUI import LightConfigUI
from UI.LightControlUI import LightControlUI
from UI.AddOBAUI import AddOBAUI
from UI.EditOBAUI import EditOBAUI
from UI.OBAConfigUI import OBAConfigUI
from UI.OBAControlUI import OBAControlUI
from UI.AddTracUI import AddTracUI
from UI.EditTracUI import EditTracUI
from UI.TracConfigUI import TracConfigUI
from UI.TracControlUI import TracControlUI
from UI.UserPrefUI import UserPrefUI
from UI.Gyro import Gyrometer


class MainUI(QWidget):

    def __init__(self):
        super().__init__()
        self.left = Config.geometry[0]
        self.top = Config.geometry[1]
        self.width = Config.geometry[2]
        self.height = Config.geometry[3]
        self.setLayout(QHBoxLayout(self))
        # Init logger
        self._logger = Logger('mainUI', 'UI : Main')
        # Read in user prefs
        self._prefs = Config.getPrefs()
        # Load configured objects
        self.lights = Lights()
        self.obas = OBAs()
        self.tracs = Tracs()
        for _ in (self.obas, self.lights, self.tracs):
            _.load()
        # Init I2C control
        self._i2cBus = I2CBus(
            self.prefs.get("i2cBus", Config.defaultI2CBus),
            self.prefs.get('i2cAddress', Config.defaultI2CAddress),
            self.prefs.get("i2cDebug", False)
        )
        # Create menu frame
        self._sidebarMenu = QFrame(self)
        self._sidebarMenu.layout = QVBoxLayout(self._sidebarMenu)
        self._sidebarMenu.setMaximumWidth(Config.menuWidth + 50)
        self._sidebarMenu.setMaximumHeight(Config.geometry[3])
        self._sidebarMenu.setStyleSheet("QFrame{border-right: 1px solid black}")
        # Create menu
        _container = QWidget()
        _container.layout = QVBoxLayout()
        _container.setLayout(_container.layout)
        _scroll = QScrollArea()
        _scroll.setWidget(_container)
        _scroll.setWidgetResizable(True)
        self._sidebarMenu.layout.addWidget(_scroll)
        for _key in ['enableOBA', 'enableLighting', 'enableTracControl', 'enableCamViewer', 'enableGyro']:
            if self.prefs.get(_key, False):
                _title = {'enableOBA': 'control_oba',
                          'enableLighting': 'control_light',
                          'enableTracControl': 'control_trac',
                          'enableCamViewer': 'control_cam',
                          'enableGyro': 'control_gyro'}[_key]
                _icon = {'enableOBA': Config.faIcon("wind"),
                         'enableLighting': Config.faIcon("lightbulb"),
                         'enableTracControl': Config.icon("tracControl", "rearDiff")['path'],
                         'enableCamViewer': Config.faIcon("camera"),
                         'enableGyro': Config.faIcon("truck-pickup")}[_key]
                _button = MenuButton(panel=_title, parent=self)
                _button.setIcon(QIcon(_icon))
                _container.layout.addWidget(_button)
        _settingsButton = MenuButton(panel="config_prefs", parent=self)
        _settingsButton.setIcon(QIcon(Config.faIcon("user-cog")))
        _container.layout.addWidget(_settingsButton)
        del _settingsButton, _title, _icon, _button
        # Create version info label
        self._version = QLabel('v%s' % Config.version, self)
        self._version.setAlignment(Qt.AlignCenter)
        self._version.setFixedWidth(Config.menuWidth)
        self._version.setStyleSheet("QLabel{border: none}")
        self._sidebarMenu.layout.addWidget(self._version)
        # Create OSK button
        self._oskButton = QPushButton('', self)
        self._oskButton.setIcon(QIcon(Config.faIcon('keyboard')))
        self._oskButton.setFixedWidth(Config.menuWidth)
        self._oskButton.clicked.connect(self.showOSK)
        self._sidebarMenu.layout.addWidget(self._oskButton)
        # Add menu frame to main UI
        self.layout().addWidget(self._sidebarMenu)
        # Create main UI panel
        self._mainPanel = QWidget(self)
        self._mainPanel.setLayout(QVBoxLayout(self._mainPanel))
        self.layout().addWidget(self._mainPanel)
        # Init default UI
        for _ in ['enableOBA', 'enableLighting', 'enableTracControl', 'enableCamViewer', 'enableGyro']:
            _cUI = None
            _uiName = None
            if self.prefs.get(_, False):
                if _ == 'enableOBA':
                    _cUI = OBAControlUI(self.obas.obas, self)
                    _uiName = 'control_oba'
                elif _ == 'enableLighting':
                    _cUI = LightControlUI(self.lights.lights, self)
                    _uiName = 'control_light'
                elif _ == 'enableTracControl':
                    _cUI = TracControlUI(self.tracs.tracs, self)
                    _uiName = 'control_trac'
                elif _ == 'enableCamViewer':
                    _cUI = CamViewer(0)
                    _uiName = 'control_cam'
                elif _ == 'enableGryo':
                    _cUI = Gyrometer()
                    _uiName = 'control_gyro'
            if _cUI is not None:
                break
        if _cUI is None:
            _cUI = UserPrefUI(self.prefs, parent=self)
            _uiName = 'config_prefs'
        self._currentUI = {'name': _uiName, 'obj': _cUI}
        _cUI.setParent(self)
        self._mainPanel.layout().addWidget(_cUI)
        _cUI.show()
        # Create button panel
        self._btnPanel = QWidget(self)
        self._btnPanel.setLayout(QHBoxLayout(self._btnPanel))
        self._mainPanel.layout().addWidget(self._btnPanel)
        # Create Config button
        self._configButton = QPushButton('Configure', self)
        self._configButton.setFixedHeight(50)
        self._configButton.setIcon(QIcon(Config.faIcon('cog')))
        self._configButton.clicked.connect(self.__configButtonAction)
        self._btnPanel.layout().addWidget(self._configButton)
        # Create Night Mode button
        self._nightModeButton = QPushButton('', self)
        self._nightModeButton.setFixedHeight(50)
        self._nightModeButton.setIcon(
            QIcon({True: Config.faIcon('sun'), False: Config.faIcon('moon')}[self.prefs['nightMode']]))
        self._nightModeButton.setText({True: 'Day Mode', False: 'Night Mode'}[self.prefs['nightMode']])
        self._nightModeButton.clicked.connect(self.toggleNightMode)
        self._btnPanel.layout().addWidget(self._nightModeButton)
        self.setNightMode(self.prefs.get('nightMode'))

    def closeEvent(self, event):
        Config.setPrefs(self.prefs)
        self.i2cBus.deEnergizeAll()
        super(MainUI, self).closeEvent(event)

    def availablePins(self):
        _pins = Config.outputPinList
        if not self.prefs.get('allowDuplicatePins', False):
            for _ in [self.lights.lights, self.obas.obas, self.tracs.tracs]:
                for __ in _:
                    if __.outputPin in _pins:
                        _pins.remove(__.outputPin)
        _pins.sort()
        return _pins

    def setOutputPin(self, pin, state):
        _fx = self.i2cBus.energizeRelay if state else self.i2cBus.deEnergizeRelay
        _fx(pin)

    def disableConfigButtons(self):
        for _ in [self.configButton]:
            _.setEnabled(False)

    def enableConfigButtons(self):
        for _ in [self.configButton]:
            _.setEnabled(True)

    def loadUI(self, ui, idx=None):
        if 'cam' in self.currentUI['name']:
            self.currentUI['obj'].stop()
        if 'gyro' in self.currentUI['name']:
            self.currentUI['obj'].stopSerial()
            self.currentUI['obj'].stopRotation()
        self.currentUI['obj'].hide()
        self.mainPanel.layout().removeWidget(self.currentUI['obj'])
        self.mainPanel.layout().removeWidget(self.btnPanel)
        _mode = ui.split('_')[0]
        _type = ui.split('_')[1]
        _ui = None
        if _mode == 'control':
            if _type == 'gyro':
                self.configButton.setText("Calibrate")
            else:
                self.configButton.setText("Configure")
            if _type == 'light':
                _ui = LightControlUI(self.lights.lights, self)
            elif _type == 'oba':
                _ui = OBAControlUI(self.obas.obas, self)
            elif _type == 'trac':
                _ui = TracControlUI(self.tracs.tracs, self)
            elif _type == 'cam':
                _ui = CamViewer(0)
                _ui.start()
            elif _type == 'gyro':
                _ui = Gyrometer(parent=self)
                _ui.startSerial()
                _ui.startRotation()
        elif _mode == 'config':
            if _type == 'light':
                _ui = LightConfigUI(self.lights.lights, self)
            elif _type == 'oba':
                _ui = OBAConfigUI(self.obas.obas, self)
            elif _type == 'trac':
                _ui = TracConfigUI(self.tracs.tracs, self)
            elif _type == 'prefs':
                _ui = UserPrefUI(self.prefs, self)
        elif _mode == 'edit':
            if _type == 'light':
                _ui = EditLightUI(self.lights.lights[idx], self)
            elif _type == 'oba':
                _ui = EditOBAUI(self.obas.obas[idx], self)
            elif _type == 'trac':
                _ui = EditTracUI(self.tracs.tracs[idx], self)
        elif _mode == 'create':
            if _type == 'light':
                _ui = AddLightUI(self)
            elif _type == 'oba':
                _ui = AddOBAUI(self)
            elif _type == 'trac':
                _ui = AddTracUI(self)
        if _ui is not None:
            _ui.setParent(self)
            self.mainPanel.layout().addWidget(_ui)
            _ui.show()
            self.currentUI = {'name': ui, 'obj': _ui}
        self.mainPanel.layout().addWidget(self.btnPanel)

    def toggleNightMode(self):
        _mode = self.prefs['nightMode']
        _value = {False: Config.dayBright, True: Config.nightBright}[not _mode]
        self.nightModeButton.setIcon({False: QIcon(Config.faIcon('sun')),
                                      True: QIcon(Config.faIcon('moon'))}
                                     [not _mode])
        self.nightModeButton.setText({False: 'Day Mode', True: 'Night Mode'}[not _mode])
        os.system("echo %s > /sys/class/backlight/rpi_backlight/brightness" % _value)
        self.prefs['nightMode'] = not _mode
        Config.setPrefs(self.prefs)
        self.logger.log('Night mode %s: backlight set to %s' % (not _mode, _value))
        del _mode, _value

    def setNightMode(self, mode):
        _value = {False: Config.dayBright, True: Config.nightBright}[mode]
        self.nightModeButton.setIcon({False: QIcon(Config.faIcon('sun')),
                                      True: QIcon(Config.faIcon('moon'))}
                                     [mode])
        self.nightModeButton.setText({False: 'Day Mode', True: 'Night Mode'}[mode])
        os.system("echo %s > /sys/class/backlight/rpi_backlight/brightness" % _value)
        del _value

    def showOSK(self):
        if self.window().dock.isHidden():
            self.window().dock.show()
        else:
            self.window().dock.hide()

    def __configButtonAction(self):
        if self.currentUI['name'] not in ['control_camera', 'control_gyro']:
            self.disableConfigButtons()
            self.mainPanel.layout().removeWidget(self.currentUI['obj'])
            self.loadUI(self.currentUI['name'].replace('control', 'config'))
        elif self.currentUI['name'] == 'control_gyro':
            self.currentUI['obj'].calibrate()

    @property
    def logger(self):
        return self._logger

    @property
    def prefs(self):
        return self._prefs

    @prefs.setter
    def prefs(self, value):
        self._prefs = value

    @property
    def mainPanel(self):
        return self._mainPanel

    @property
    def btnPanel(self):
        return self._btnPanel

    @property
    def nightModeButton(self):
        return self._nightModeButton

    @property
    def configButton(self):
        return self._configButton

    @property
    def currentUI(self):
        return self._currentUI

    @currentUI.setter
    def currentUI(self, value):
        self._currentUI = value

    @property
    def i2cBus(self):
        return self._i2cBus
