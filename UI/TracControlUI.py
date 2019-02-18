"""
=====================
TacOS Trac Control UI
=====================

Provides a control interface for enabled Trac objects in the TacOS environment.

"""

import pyforms
import pickle
from pyforms.basewidget import BaseWidget
from pyforms.basewidget import no_columns
from Objects import Config
from Objects.TracControl import TracControl
from Objects.Logger import Logger
from UI.TracConfigUI import TracConfigUI


def group(n, l):
    """
    Group a list into n tuples.
    :param n: Qty to group by.
    :type n: int
    :param l: List to group.
    :type l: list
    :return: A list of tuples of len <= n.
    :rtype: list
    """
    return [tuple(l[i:i+n]) for i in range(0, len(l), n)]


class TracControlUI(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'Light Configuration')

        self._logger = Logger('tracControl', "UI : TracControl")

        # Init permanent controls

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
            x = TracControl(label=self._tracs[key]['name'])
            exec("self._%s = x" % key)
            control = eval('self._%s' % key)
            control.parent = self
            control.icon = Config.icon('tracControl', self._tracs[key]['icon'])['path']
            keyStrings.append('_%s' % key)

        # Control settings

        # Assign button callback fx

        # Build dynamic formset
        formset = "self._formset = ["
        for item in group(Config.tracColumns, keyStrings):
            if len(item) > 1:
                formset = formset + 'no_columns' + str(item) + ','
            else:
                formset = formset + 'no_columns' + str(item)[:-2] + '),'

        formset += "]"
        exec(formset)

        msg = 'TacOS TracControl UI initialized successfully'
        self._logger.log(msg)

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
                self.parent.setOutputPin(self._tracs[key]['outputPin'], state)
                break

    def configBtnAction(self):
        win = TracConfigUI()
        win.parent = self.parent
        self.parent.tracPanel.value = win

    def __settings(self):
        self.parent.settings()

    @property
    def tracs(self):
        return self._tracs

    @tracs.setter
    def tracs(self, value):
        """
        :type value: dict
        """
        self._tracs = value


if __name__ == '__main__':
    pyforms.start_app(TracControlUI)
