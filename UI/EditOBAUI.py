"""
================
TacOS EditOBA UI
================

Extends the TacOS OBA class to provide a UI to reconfigure OBA Element objects in the TacOS environment.

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


class EditOBAUI(OBA, BaseWidget):

    def __init__(self, name, outputPin, enabled, icon, momentary, index, availablePins):
        OBA.__init__(self, name, outputPin, enabled, icon)
        BaseWidget.__init__(self, 'Edit OBA Element')

        self._nameControl = ControlText('Name')
        self._outputPinControl = ControlCombo('Output Pin')
        self._momentaryControl = ControlCheckBox('Momentary')
        self._enabledControl = ControlCheckBox('Enabled')
        self._iconControl = IconCombo('Icon Path')
        self._saveBtn = ControlButton('Save')
        self._cancelBtn = ControlButton('Cancel')
        self._index = int(index)

        # Init list of available output pins
        for x in availablePins:
            self._outputPinControl.add_item(str(x))

        # Init list of icons
        i = 0
        for key in Config.icons['oba'].keys():
            icon = Config.icon('oba', key)
            self._iconControl.add_item(icon['name'], key)
            self._iconControl.setItemIcon(i, icon['path'])
            i += 1

        # Def callback fx for button
        self._saveBtn.value = self.__saveBtnAction
        self._cancelBtn.value = self.__cancel

        # Init control values
        self._nameControl.value = self.name
        self._outputPinControl.value = self.outputPin
        self._enabledControl.value = self.enabled
        self._iconControl.value = self.icon
        self._momentaryControl.value = self.momentary

        # Arrange controls
        self._formset = [
            '_nameControl',
            '_outputPinControl',
            ('_momentaryControl', '_enabledControl'),
            '_iconControl',
            ('_saveBtn', '_cancelBtn')
        ]

    def __saveBtnAction(self):
        self._name = self._nameControl.value
        self._outputPin = self._outputPinControl.value
        self._enabled = self._enabledControl.value
        self._icon = self._iconControl.value
        self._momentary = self._momentaryControl.value

        if self.parent is not None:
            self.parent.editOBA(self, self._index)

    def __cancel(self):
        self.close()
        if self.parent is not None:
            self.parent.parent.obaPanel.value = self.parent


if __name__ == '__main__':
    pyforms.start_app(EditOBAUI)
