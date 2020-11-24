"""
======================
TacOS Light Control UI
======================

Provides a control interface for enabled Light objects in the TacOS environment.

"""

import pickle
from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from AnyQt.QtGui import QIcon
from Objects import Config, Tools
from Objects.LightControl import LightControl
from Objects.Logger import Logger


class LightControlUI(QWidget):

    def __init__(self, parent=None):
        super(LightControlUI, self).__init__()
        self.title = 'Light Control UI'
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._parent = parent

        self._logger = Logger('lightControl', "UI : LightControl")

        # Init internal Lights dict
        self._lights = {}

        # Read in configured lights
        lcfg = open(Config.lightConfig, 'rb')
        rawLights = pickle.load(lcfg)
        for key in rawLights.keys():
            # Add enabled lights to internal dict
            if rawLights[key]['enabled']:
                if 'strobe' in rawLights[key].keys():
                    strobe = rawLights[key]['strobe']
                else:
                    strobe = False
                self._lights[key] = {'name': rawLights[key]['name'],
                                     'outputPin': rawLights[key]['outputPin'],
                                     'active': False,
                                     'icon': rawLights[key]['icon'],
                                     'strobe': strobe
                                     }
        lcfg.close()

        # Dynamically generate controls
        keyStrings = []
        for key in self._lights.keys():
            x = LightControl(self._lights[key]['name'], parent=self, strobe=self._lights[key]['strobe'])
            exec("self._%s = x" % key)
            control = eval('self._%s' % key)
            control.setParent(self)
            control.setIcon(QIcon(Config.icon('lights', self._lights[key]['icon'])['path']))
            keyStrings.append('_%s' % key)

        # Organize controls in groups of tuples
        oList = Tools.group(Config.lightColumns, keyStrings)

        # Dynamically generate panel layout using grouped tuples
        for oTuple in oList:
            # Create panel and set HBox layout
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            for oWidget in oTuple:
                panel.layout.addWidget(eval('self.%s' % oWidget))
            self.layout.addWidget(panel)
            del panel

    def refresh(self):
        self.__init__()

    def setLight(self, name, state):
        """
        Set the output state for a given light.
        :param name: The display name of the light.
        :type name : str
        :param state: The state to set.
        :type state: bool
        """
        for key in self._lights.keys():
            if self._lights[key]['name'] == name:
                self._lights[key]['active'] = state
                self._parent.setOutputPin(self._lights[key]['outputPin'], state)
                break

    @property
    def lights(self):
        return self._lights

    @lights.setter
    def lights(self, value):
        """
        :type value: dict
        """
        self._lights = value
