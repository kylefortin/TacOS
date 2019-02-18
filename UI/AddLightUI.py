"""
=================
TacOS AddLight UI
=================

Extends the TacOS Light class to provide a UI to configure a Light in the TacOS environment.

"""

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlCombo
from pyforms.controls import ControlText

from Objects import Config
from Objects.Light import Light
from Objects.IconCombo import IconCombo


class AddLightUI(Light, BaseWidget):

    def __init__(self, availablePins):
        Light.__init__(self, '', 0, False, Config.faIcon('lightbulb'))
        BaseWidget.__init__(self, 'Create Light')

        self._nameControl = ControlText('Name')
        self._outputPinControl = ControlCombo('Output Pin')
        self._enabledControl = ControlCheckBox('Enabled')
        self._iconControl = IconCombo('Icon')
        self._addLightBtn = ControlButton('Add Light')
        self._cancelBtn = ControlButton('Cancel')

        # Init list of available output pins
        for x in availablePins:
            self._outputPinControl.add_item(str(x))
        self._outputPinControl.value = self._outputPin

        # Init list of icons
        i = 0
        for key in Config.icons['lights'].keys():
            icon = Config.icon('lights', key)
            self._iconControl.add_item(icon['name'], key)
            self._iconControl.setItemIcon(i, icon['path'])
            i += 1

        # Def callback fx for button
        self._addLightBtn.value = self.__createLightBtnAction
        self._cancelBtn.value = self.__cancel

        # Set layout
        self._formset = [
            '_nameControl',
            '_outputPinControl',
            '_enabledControl',
            '_iconControl',
            ('_addLightBtn', '_cancelBtn')
        ]

    def __createLightBtnAction(self):
        self._name = self._nameControl.value
        self._outputPin = int(self._outputPinControl.value)
        self._enabled = self._enabledControl.value
        self._icon = self._iconControl.value

        if self.parent is not None:
            self.parent.createTrac(self)

    def __cancel(self):
        self.close()
        if self.parent is not None:
            self.parent.parent.lightPanel.value = self.parent


if __name__ == '__main__':
    pyforms.start_app(AddLightUI)
