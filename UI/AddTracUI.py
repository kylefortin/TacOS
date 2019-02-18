"""
================
TacOS AddTrac UI
================

Extends the TacOS Trac class to provide a UI to configure a Trac in the TacOS environment.

"""

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlCombo
from pyforms.controls import ControlText

from Objects import Config
from Objects.Trac import Trac
from Objects.IconCombo import IconCombo


class AddTracUI(Trac, BaseWidget):

    def __init__(self, availablePins):
        Trac.__init__(self, '', 0, False, Config.icon('tracControl', 'rearDiff'))
        BaseWidget.__init__(self, 'Create TracControl')

        self._nameControl = ControlText('Name')
        self._outputPinControl = ControlCombo('Output Pin')
        self._enabledControl = ControlCheckBox('Enabled')
        self._iconControl = IconCombo('Icon')
        self._addTracBtn = ControlButton('Add TracControl')
        self._cancelBtn = ControlButton('Cancel')

        # Init list of available output pins
        for x in availablePins:
            self._outputPinControl.add_item(str(x))
        self._outputPinControl.value = self._outputPin

        # Init list of icons
        i = 0
        for key in Config.icons['tracControl'].keys():
            icon = Config.icon('tracControl', key)
            self._iconControl.add_item(icon['name'], key)
            self._iconControl.setItemIcon(i, icon['path'])
            i += 1

        # Def callback fx for button
        self._addTracBtn.value = self.__createTracBtnAction
        self._cancelBtn.value = self.__cancel

        # Set layout
        self._formset = [
            '_nameControl',
            '_outputPinControl',
            '_enabledControl',
            '_iconControl',
            ('_addTracBtn', '_cancelBtn')
        ]

    def __createTracBtnAction(self):
        self._name = self._nameControl.value
        self._outputPin = int(self._outputPinControl.value)
        self._enabled = self._enabledControl.value
        self._icon = self._iconControl.value

        if self.parent is not None:
            self.parent.createTrac(self)

    def __cancel(self):
        self.close()
        if self.parent is not None:
            self.parent.parent.tracPanel.value = self.parent


if __name__ == '__main__':
    pyforms.start_app(AddTracUI)
