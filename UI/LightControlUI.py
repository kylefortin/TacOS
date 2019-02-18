"""
======================
TacOS Light Control UI
======================

Provides a control interface for enabled Light objects in the TacOS environment.

"""

import pyforms
import pickle
from pyforms.basewidget import BaseWidget
from pyforms.basewidget import no_columns
from Objects import Config
from Objects.LightControl import LightControl
from Objects.Logger import Logger
from UI.LightConfigUI import LightConfigUI


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


class LightControlUI(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'Light Configuration')

        self._logger = Logger('lightControl', "UI : LightControl")

        # Init permanent controls

        # Init internal Lights dict
        self._lights = {}

        # Read in configured lights
        lcfg = open(Config.lightConfig, 'rb')
        rawLights = pickle.load(lcfg)
        for key in rawLights.keys():
            # Add enabled lights to internal dict
            if rawLights[key]['enabled']:
                self._lights[key] = {'name': rawLights[key]['name'],
                                     'outputPin': rawLights[key]['outputPin'],
                                     'active': False,
                                     'icon': rawLights[key]['icon']
                                     }
        lcfg.close()

        # Dynamically generate controls
        keyStrings = []
        for key in self._lights.keys():
            x = LightControl(label=self._lights[key]['name'])
            exec("self._%s = x" % key)
            control = eval('self._%s' % key)
            control.parent = self
            control.icon = Config.icon('lights', self._lights[key]['icon'])['path']
            keyStrings.append('_%s' % key)

        # Control settings

        # Assign button callback fx

        # Build dynamic formset
        formset = "self._formset = ["
        for item in group(Config.lightColumns, keyStrings):
            if len(item) > 1:
                formset = formset + 'no_columns' + str(item) + ','
            else:
                formset = formset + 'no_columns' + str(item)[:-2] + '),'

        formset += "]"
        exec(formset)

        msg = 'TacOS LightControl UI initialized successfully'
        self._logger.log(msg)

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
                self.parent.setOutputPin(self._lights[key]['outputPin'], state)
                break

    def configBtnAction(self):
        win = LightConfigUI()
        win.parent = self.parent
        self.parent.lightPanel.value = win

    @property
    def lights(self):
        return self._lights

    @lights.setter
    def lights(self, value):
        """
        :type value: dict
        """
        self._lights = value


if __name__ == '__main__':
    pyforms.start_app(LightControlUI)
