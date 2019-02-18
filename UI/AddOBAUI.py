"""
=================
TacOS AddOBA UI
=================

Extends the TacOS OBA class to provide a UI to configure an OBA Element in the TacOS environment.

"""

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlCombo
from pyforms.controls import ControlText

from Objects import Config
from Objects.OBA import OBA
from Objects.IconCombo import IconCombo


class AddOBAUI(OBA, BaseWidget):

    def __init__(self, availablePins):
        OBA.__init__(self, '', 0, False, Config.icon('oba', 'airhose'), False)
        BaseWidget.__init__(self, 'Create OBA Element')

        self._nameControl = ControlText('Name')
        self._outputPinControl = ControlCombo('Output Pin')
        self._momentaryControl = ControlCheckBox('Momentary')
        self._enabledControl = ControlCheckBox('Enabled')
        self._iconControl = IconCombo('Icon')
        self._addOBABtn = ControlButton('Add OBA Element')
        self._cancelBtn = ControlButton('Cancel')

        # Init list of available output pins
        for x in availablePins:
            self._outputPinControl.add_item(str(x))
        self._outputPinControl.value = self._outputPin

        # Init list of icons
        i = 0
        for key in Config.icons['oba'].keys():
            icon = Config.icon('oba', key)
            self._iconControl.add_item(icon['name'], key)
            self._iconControl.setItemIcon(i, icon['path'])
            i += 1

        # Def callback fx for button
        self._addOBABtn.value = self.__createOBABtnAction
        self._cancelBtn.value = self.__cancel

        # Set layout
        self._formset = [
            '_nameControl',
            '_outputPinControl',
            ('_momentaryControl', '_enabledControl'),
            '_iconControl',
            ('_addOBABtn', '_cancelBtn')
        ]

    def __createOBABtnAction(self):
        self._name = self._nameControl.value
        self._outputPin = int(self._outputPinControl.value)
        self._enabled = self._enabledControl.value
        self._icon = self._iconControl.value
        self._momentary = self._momentaryControl.value

        if self.parent is not None:
            self.parent.createOBA(self)

    def __cancel(self):
        self.close()
        if self.parent is not None:
            self.parent.parent.obaPanel.value = self.parent


if __name__ == '__main__':
    pyforms.start_app(AddOBAUI)
