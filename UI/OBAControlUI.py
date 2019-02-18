"""
====================
TacOS OBA Control UI
====================

Provides a control interface for enabled OBA objects in the TacOS environment.

"""

import pyforms
import pickle
from pyforms.basewidget import BaseWidget
from pyforms.basewidget import no_columns
from Objects import Config
from Objects.OBAControl import OBAControl
from Objects.Logger import Logger
from UI.OBAConfigUI import OBAConfigUI


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
    return [tuple(l[i:i + n]) for i in range(0, len(l), n)]


class OBAControlUI(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'OnBoard Air Control Interface')

        self._logger = Logger('obaControl', "UI : OBAControl")

        # Init permanent controls

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

        del rawOBAs

        obaFormset = ()

        # Dynamically generate controls
        keyStrings = []
        for key in self._obas.keys():
            x = OBAControl(label=self._obas[key]['name'], momentary=self._obas[key]['momentary'])
            exec("self._%s = x" % key)
            control = eval('self._%s' % key)
            control.parent = self
            control.icon = Config.icon('oba', self._obas[key]['icon'])['path']
            obaFormset = obaFormset + ('_%s' % key,)
            keyStrings.append('_%s' % key)

        # Control settings

        # Assign button callback fx

        # Build dynamic formset
        formset = "self._formset = ["
        for item in group(Config.obaColumns, keyStrings):
            if len(item) > 1:
                formset = formset + 'no_columns' + str(item) + ','
            else:
                formset = formset + 'no_columns' + str(item)[:-2] + '),'

        formset += "]"
        exec(formset)

        msg = 'TacOS OBAControl UI initialized successfully'
        self._logger.log(msg)

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
                self.parent.setOutputPin(self._obas[key]['outputPin'], state)
                break

    def configBtnAction(self):
        win = OBAConfigUI()
        win.parent = self.parent
        self.parent.obaPanel.value = win

    @property
    def obas(self):
        return self._obas

    @obas.setter
    def obas(self, value):
        """
        :type value: dict
        """
        self._obas = value


if __name__ == '__main__':
    pyforms.start_app(OBAControlUI)
