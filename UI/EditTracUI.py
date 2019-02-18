"""
=================
TacOS EditTrac UI
=================

Extends the TacOS Trac class to provide a UI to reconfigure Trac objects in the TacOS environment.

"""

from Objects import Config
import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlCombo
from pyforms.controls import ControlText

from Objects.Trac import Trac
from Objects.IconCombo import IconCombo


class EditTracUI(Trac, BaseWidget):

    def __init__(self, name, outputPin, enabled, icon, index, availablePins):
        Trac.__init__(self, name, outputPin, enabled, icon)
        BaseWidget.__init__(self, 'Add Light')

        self._nameControl = ControlText('Name')
        self._outputPinControl = ControlCombo('Output Pin')
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
        for key in Config.icons['tracControl'].keys():
            icon = Config.icon('tracControl', key)
            self._iconControl.add_item(icon['name'], key)
            self._iconControl.setItemIcon(i, icon['path'])
            i += 1

        # Def callback fx for button
        self._saveBtn.value = self.__saveBtnAction
        self._cancelBtn.value = self.__cancel

        # Init control values
        self._nameControl.value = name
        self._outputPinControl.value = outputPin
        self._enabledControl.value = enabled
        self._iconControl.value = icon

        # Arrange controls
        self._formset = [
            '_nameControl',
            '_outputPinControl',
            '_enabledControl',
            '_iconControl',
            ('_saveBtn', '_cancelBtn')
        ]

    def __saveBtnAction(self):
        self._name = self._nameControl.value
        self._outputPin = self._outputPinControl.value
        self._enabled = self._enabledControl.value
        self._icon = self._iconControl.value

        if self.parent is not None:
            self.parent.editTrac(self, self._index)

    def __cancel(self):
        self.close()
        if self.parent is not None:
            self.parent.parent.tracPanel.value = self.parent


if __name__ == '__main__':
    pyforms.start_app(EditTracUI)
