"""
====================
TacOS OBA Control UI
====================

Provides a control interface for enabled OBA objects in the TacOS environment.

"""

import pickle
from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from AnyQt.QtGui import QIcon
from Objects import Config, Tools
from Objects.OBAControl import OBAControl
from Objects.Logger import Logger


class OBAControlUI(QWidget):

    def __init__(self, parent=None):
        super(OBAControlUI, self).__init__()
        self.title = 'OnBoar Air Control UI'
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._parent = parent

        self._logger = Logger('obaControl', "UI : OBAControl")

        # Read in configured OBA elements
        obacfg = open(Config.obaConfig, 'rb')
        rawOBAs = pickle.load(obacfg)
        self._obas = {}
        for key in rawOBAs.keys():
            # Add enabled OBA elements to internal dict
            if rawOBAs[key]['enabled']:
                self._obas[key] = {'name': rawOBAs[key]['name'],
                                   'outputPin': rawOBAs[key]['outputPin'],
                                   'momentary': rawOBAs[key]['momentary'],
                                   'active': False,
                                   'icon': rawOBAs[key]['icon']
                                   }
        obacfg.close()

        # Dynamically generate controls
        keyStrings = []
        for key in self._obas.keys():
            x = OBAControl(self._obas[key]['name'], momentary=self._obas[key]['momentary'], parent=self)
            exec("self._%s = x" % key)
            control = eval('self._%s' % key)
            control.setIcon(QIcon(Config.icon('oba', self._obas[key]['icon'])['path']))
            keyStrings.append('_%s' % key)

        # Organize controls in groups of tuples
        oList = Tools.group(Config.obaColumns, keyStrings)

        # Dynamically generate panel layout using grouped tuples
        for oTuple in oList:
            # Create panel and set HBox layout
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            for oWidget in oTuple:
                panel.layout.addWidget(eval('self.%s' % oWidget))
            self.layout.addWidget(panel)
            del panel

    def setOBA(self, name, state):
        """
        :param state: State to set OBA element to.
        :type state: bool
        :param name: The display name of the light to toggle.
        :type name : str
        """
        for key in self._obas.keys():
            if self._obas[key]['name'] == name:
                self._obas[key]['active'] = state
                self._parent.setOutputPin(self._obas[key]['outputPin'], state)
                break

    @property
    def obas(self):
        return self._obas

    @obas.setter
    def obas(self, value):
        """
        :type value: dict
        """
        self._obas = value
