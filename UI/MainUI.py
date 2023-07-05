"""
=============
TacOS Main UI
=============

The main UI for the TacOS environment.  Envelops all other window modules in a docked frame.

"""

import os
from AnyQt.QtCore import Qt
from AnyQt.QtGui import QIcon
from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLabel, QFrame, QScrollArea
from Objects import Config
from Objects.Lights import Lights
from Objects.OBAs import OBAs
from Objects.Tracs import Tracs
from Objects.MenuButton import MenuButton
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
from UI.CamViewerUI import CamViewerUI


class MainUI(QWidget):

    def __init__(self):
        super().__init__()
        # Init logger
        self._logger = Logger('mainUI', 'UI : Main')
        # Init geometry
        _geometry = {"left": Config.geometry[0], "top": Config.geometry[1],
                     "width": Config.geometry[2], "height": Config.geometry[3]}
        for k, v in _geometry.items():
            exec("%s = v" % k)
        del _geometry
        self.setLayout(QHBoxLayout(self))
        # Read in user prefs
        self._prefs = Config.getPrefs()
        # Load configured objects
        self.lights = Lights()
        self.obas = OBAs()
        self.tracs = Tracs()
        for _ in (self.obas, self.lights, self.tracs):
            _.load()
        # Init I2C control
        self._i2cBus = I2CBus(self)
        # Create menu frame
        sidebarMenu = QFrame(self)
        sidebarMenu.layout = QVBoxLayout(sidebarMenu)
        sidebarMenu.setMaximumWidth(Config.menuWidth + 50)
        sidebarMenu.setMaximumHeight(Config.geometry[3])
        sidebarMenu.setStyleSheet("QFrame{border-right: 1px solid black}")
        # Create menu
        container = QWidget()
        container.layout = QVBoxLayout()
        container.setLayout(container.layout)
        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        sidebarMenu.layout.addWidget(scroll)
        del scroll
        configs = {"enableOBA": ("control_oba", Config.faIcon("wind")),
                   "enableLighting": ("control_light", Config.faIcon("lightbulb")),
                   "enableTracControl": ("control_trac", Config.icon("tracControl", "rearDiff")['path']),
                   "enableCamViewer": ("control_cam", Config.faIcon("camera")),
                   "enableGyro": ("control_gyro", Config.faIcon("truck-pickup"))}
        for k, v in configs.items():
            if self.prefs.get(k, False):
                button = MenuButton(panel=v[0], parent=self)
                button.setIcon(QIcon(v[1]))
                container.layout.addWidget(button)
        del button, configs, k, v
        settingsButton = MenuButton(panel="config_prefs", parent=self)
        settingsButton.setIcon(QIcon(Config.faIcon("user-cog")))
        container.layout.addWidget(settingsButton)
        del settingsButton, container
        # Create version info label
        version = QLabel('v%s' % Config.version, self)
        version.setAlignment(Qt.AlignCenter)
        version.setFixedWidth(Config.menuWidth)
        version.setStyleSheet("QLabel{border: none}")
        sidebarMenu.layout.addWidget(version)
        del version
        # Create OSK button
        oskButton = QPushButton('', self)
        oskButton.setIcon(QIcon(Config.faIcon('keyboard')))
        oskButton.setFixedWidth(Config.menuWidth)
        oskButton.clicked.connect(self.showOSK)
        sidebarMenu.layout.addWidget(oskButton)
        del oskButton
        # Add menu frame to main UI
        self.layout().addWidget(sidebarMenu)
        # Create main UI panel
        self._mainPanel = QWidget(self)
        self.mainPanel.setLayout(QVBoxLayout(self.mainPanel))
        self.layout().addWidget(self.mainPanel)
        # Init default UI
        cUI = None
        uiName = None
        modules = {'enableOBA': (OBAControlUI, [self], 'control_oba'),
                   'enableLighting': (LightControlUI, [self], 'control_light'),
                   'enableTracControl': (TracControlUI, [self], "control_trac"),
                   'enableCamViewer': (CamViewerUI, [self], "control_cam"),
                   'enableGyro': (Gyrometer, [self], "control_gyro")}
        for k, v in modules.items():
            v: tuple[type, list, str]
            if self.prefs.get(k, False):
                cUI = v[0](*v[1])
                uiName = v[2]
                break
        if cUI is None:
            cUI = UserPrefUI(self.prefs)
            uiName = 'config_prefs'
        self._currentUI = {'name': uiName, 'obj': cUI}
        del cUI, uiName
        self.currentUI['obj'].setParent(self)
        self.mainPanel.layout().addWidget(self.currentUI['obj'])
        self.currentUI['obj'].show()
        # Create button panel
        self._btnPanel = QWidget(self)
        self.btnPanel.setLayout(QHBoxLayout(self.btnPanel))
        self.mainPanel.layout().addWidget(self.btnPanel)
        # Create Config button
        self._configButton = QPushButton('Configure', self)
        self._configButton.setFixedHeight(50)
        self._configButton.setIcon(QIcon(Config.faIcon('cog')))
        self._configButton.clicked.connect(self.__configButtonAction)
        self.btnPanel.layout().addWidget(self._configButton)
        # Create Night Mode button
        self._nightModeButton = QPushButton('', self)
        self._nightModeButton.setFixedHeight(50)
        self._nightModeButton.setIcon(
            QIcon({True: Config.faIcon('sun'), False: Config.faIcon('moon')}[self.prefs['nightMode']]))
        self._nightModeButton.setText({True: 'Day Mode', False: 'Night Mode'}[self.prefs['nightMode']])
        self._nightModeButton.clicked.connect(self.toggleNightMode)
        self.btnPanel.layout().addWidget(self._nightModeButton)
        self.setNightMode(self.prefs.get('nightMode'))

    def closeEvent(self, event):
        Config.setPrefs(self.prefs)
        self.i2cBus.deEnergizeAll()
        super(MainUI, self).closeEvent(event)

    def availablePins(self, obj=None):
        if not self.prefs.get('allowDuplicatePins', False):
            used_pins = list()
            for obj_list in (self.lights.lights, self.obas.obas, self.tracs.tracs):
                used_pins.extend([obj.outputPin for obj in obj_list])
            pins = [pin for pin in Config.outputPinList if pin not in used_pins]
            del used_pins, obj_list
            if obj is not None:
                pins.append(obj.outputPin)
        else:
            pins = Config.outputPinList
        pins.sort()
        return pins

    def setOutputPin(self, relay: int, state: bool):
        if state:
            return self.i2cBus.energizeRelay(relay)
        else:
            return self.i2cBus.deEnergizeRelay(relay)

    def disableConfigButtons(self):
        objs = [self.configButton]
        for obj in objs:
            obj.setEnabled(False)
        del objs, obj

    def enableConfigButtons(self):
        objs = [self.configButton]
        for obj in objs:
            obj.setEnabled(True)
        del objs, obj

    def loadUI(self, ui, idx=None):
        if 'cam' in self.currentUI['name']:
            self.currentUI['obj'].stop()
        if 'gyro' in self.currentUI['name']:
            self.currentUI['obj'].stopSerial()
            self.currentUI['obj'].stopRotation()
        self.currentUI['obj'].hide()
        self.mainPanel.layout().removeWidget(self.currentUI['obj'])
        self.mainPanel.layout().removeWidget(self.btnPanel)
        ui_mode = ui.split('_')[0]
        ui_type = ui.split('_')[1]
        available_uis = {
            "control": {
                "light": (LightControlUI, [self]),
                "oba": (OBAControlUI, [self]),
                "trac": (TracControlUI, [self]),
                "cam": (CamViewerUI, [self]),
                "gyro": (Gyrometer, [self])
            },
            "config": {
                "light": (LightConfigUI, [self]),
                "oba": (OBAConfigUI, [self]),
                "trac": (TracConfigUI, [self]),
                "prefs": (UserPrefUI, [self])
            },
            "edit": {
                "light": (EditLightUI, [idx, self]),
                "oba": (EditOBAUI, [idx, self]),
                "trac": (EditTracUI, [idx, self])
            },
            "create": {
                "light": (AddLightUI, [self]),
                "oba": (AddOBAUI, [self]),
                "trac": (AddTracUI, [self])
            }
        }
        v = available_uis.get(ui_mode, {}).get(ui_type, tuple())
        v: tuple[type, list]
        new_ui = v[0](*v[1])
        new_ui.setParent(self)
        # UI special cases
        if ui_mode == "control":
            if ui_type == "gyro":
                new_ui.startSerial()
                new_ui.startRotation()
        if ui_type in ["cam", "prefs"]:
            self.disableConfigButtons()
        else:
            self.enableConfigButtons()
        if ui_type == "gyro":
            self.configButton.setText("Calibrate")
        else:
            self.configButton.setText("Configure")
        self.mainPanel.layout().addWidget(new_ui)
        new_ui.show()
        self.currentUI = {'name': ui, 'obj': new_ui}
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
