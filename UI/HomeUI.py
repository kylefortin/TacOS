"""
=============
TacOS Home UI
=============

The 'home' UI for the TacOS environment.  Allows swapping between available modules.

"""

import pyforms
from Objects import Config
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from UI.LightControlUI import LightControlUI
from Objects.Logger import Logger


class HomeUI(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'TacOS')

        self._logger = Logger('homeUI', 'UI : Home')
        self._lightBtn = ControlButton('Lighting')
        self._obaBtn = ControlButton('OnBoard Air')

        # Assign control properties
        self._lightBtn.icon = Config.lightImage
        self._obaBtn.icon = Config.OBAImage

        # Assign button functions
        self._lightBtn.value = self.__lightBtnAction
        self._obaBtn.value = self.__obaBtnAction

    def __obaBtnAction(self):
        pass

    def __lightBtnAction(self):
        self.parent.reload('LightControlUI')


if __name__ == '__main__':
    pyforms.start_app(HomeUI)
