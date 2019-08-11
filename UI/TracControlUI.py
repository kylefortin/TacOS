"""
=====================
TacOS Trac Control UI
=====================

Provides a control interface for enabled Trac objects in the TacOS environment.

"""

import pickle
from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from AnyQt.QtGui import QIcon
from Objects import Config, Tools
from Objects.TracControl import TracControl
from Objects.Logger import Logger


class TracControlUI(QWidget):

    def __init__(self, parent=None):
        super(TracControlUI, self).__init__()
        self.title = 'Light Configuration'
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._parent = parent

        self._logger = Logger('tracControl', "UI : TracControl")

        # Init internal Lights dict
        self._tracs = {}

        # Read in configured lights
        tcfg = open(Config.tracConfig, 'rb')
        rawTracs = pickle.load(tcfg)
        for key in rawTracs.keys():
            # Add enabled tracs to internal dict
            if rawTracs[key]['enabled']:
                self._tracs[key] = {'name': rawTracs[key]['name'],
                                     'outputPin': rawTracs[key]['outputPin'],
                                     'active': False,
                                     'icon': rawTracs[key]['icon']
                                    }
        tcfg.close()

        # Dynamically generate controls
        keyStrings = []
        for key in self._tracs.keys():
            x = TracControl(self._tracs[key]['name'], parent=self)
            exec("self._%s = x" % key)
            control = eval('self._%s' % key)
            control.setParent(self)
            control.setIcon(QIcon(Config.icon('tracControl', self._tracs[key]['icon'])['path']))
            keyStrings.append('_%s' % key)

        # Organize controls in groups of tuples
        oList = Tools.group(Config.tracColumns, keyStrings)

        # Dynamically generate panel layout using grouped tuples
        for oTuple in oList:
            # Create panel and set HBox layout
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            for oWidget in oTuple:
                panel.layout.addWidget(eval('self.%s' % oWidget))
            self.layout.addWidget(panel)
            del panel

    def setTrac(self, name, state):
        """
        Set the output state for a given trac.
        :param name: The display name of the trac.
        :type name : str
        :param state: The state to set.
        :type state: bool
        """
        for key in self._tracs.keys():
            if self._tracs[key]['name'] == name:
                self._tracs[key]['active'] = state
                self._parent.setOutputPin(self._tracs[key]['outputPin'], state)
                break

    @property
    def tracs(self):
        return self._tracs

    @tracs.setter
    def tracs(self, value):
        """
        :type value: dict
        """
        self._tracs = value
