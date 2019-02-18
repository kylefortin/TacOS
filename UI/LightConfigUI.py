"""
============================
TacOS Light Configuration UI
============================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

import pyforms
from Objects.Lights import Lights
from Objects.Logger import Logger
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList
from pyforms.controls import ControlButton
from UI.AddLightUI import AddLightUI
from UI.EditLightUI import EditLightUI


class LightConfigUI(Lights, BaseWidget):

    def __init__(self):
        Lights.__init__(self)
        BaseWidget.__init__(self, 'Light Configuration')

        self._logger = Logger('lightConfig', "UI : LightConfig")

        self._lightsList = ControlList('Lights',
                                       add_function=self.__createLight,
                                       remove_function=self.__destroyLight
                                       )
        self._editBtn = ControlButton('Edit')
        self._closeBtn = ControlButton('Close')

        # Control settings
        self._lightsList.horizontal_headers = ['Name', 'Output Pin', 'Enabled', 'Icon']
        self._lightsList.readonly = True
        self._lightsList.select_entire_row = True

        # Assign button callback fx
        self._editBtn.value = self.__editLight
        self._closeBtn.value = self.__closeBtnAction
        self.load()

        self.formset = [
            '_lightsList',
            '_editBtn',
            '_closeBtn'
        ]

        msg = 'TacOS LightConfig UI initialized successfully'
        self._logger.log(msg)

    def closeEvent(self, event):
        self.save()
        self._logger.log('Terminating TacOS LightConfig UI')

    def addLight(self, light):
        super(LightConfigUI, self).addLight(light)
        self._lightsList += [light.name, light.outputPin, light.enabled, light.icon]
        msg = 'Loaded preconfigured Light : %s, %s, %s, %s' % (
            light.name,
            light.outputPin,
            light.enabled,
            light.icon
        )
        self._logger.log(msg)

    def editLight(self, light, index):
        super(LightConfigUI, self).editLight(light, index)
        self._lightsList.set_value(0, index, light.name)
        self._lightsList.set_value(1, index, light.outputPin)
        self._lightsList.set_value(2, index, light.enabled)
        self._lightsList.set_value(3, index, light.icon)
        light.close()
        msg = 'Updated Light at index %s : %s, %s, %s, %s' % (
            index,
            light.name,
            light.outputPin,
            light.enabled,
            light.icon
        )
        self._logger.log(msg)
        self.updateUI()

    def createLight(self, light):
        super(LightConfigUI, self).createLight(light)
        self._lightsList += [light.name, light.outputPin, light.enabled, light.icon]
        light.close()
        msg = 'Created new Light : %s, %s, %s, %s' % (
            light.name,
            light.outputPin,
            light.enabled,
            light.icon
        )
        self._logger.log(msg)
        self.updateUI()

    def rmLight(self, index):
        super(LightConfigUI, self).rmLight(index)
        self._lightsList -= index
        msg = 'Removed Light at index %s' % (
            index
        )
        self._logger.log(msg)

    def updateUI(self):
        self.close()
        self.parent.redrawLightPanel(self.parent.LightControlUI.lights)
        win = LightConfigUI()
        win.parent = self.parent
        self.parent.lightPanel.value = win

    def __createLight(self):
        win = AddLightUI(availablePins=self.parent.availablePins())
        win.parent = self
        msg = 'Transferring to AddLight UI'
        self._logger.log(msg)
        self.parent.disableConfigButtons()
        self.parent.lightPanel.value = win

    def __destroyLight(self):
        rows = self._lightsList.selected_rows_indexes
        names = []
        for i in rows:
            names.append(self._lightsList.get_value(0, i))
        for name in names:
            for n in range(self._lightsList.rows_count):
                if self._lightsList.get_value(0, n) == name:
                    self.rmLight(n)
        self.updateUI()

    def __editLight(self):
        selectedIndex = self._lightsList.selected_row_index
        if selectedIndex is not None:
            selectedName = self._lightsList.get_value(0, selectedIndex)
            selectedOutputPin = str(self._lightsList.get_value(1, selectedIndex))
            selectedEnabled = self._lightsList.get_value(2, selectedIndex) != 'false'
            selectedIcon = self._lightsList.get_value(3, selectedIndex)
            win = EditLightUI(selectedName, selectedOutputPin, selectedEnabled, selectedIcon,
                              selectedIndex, self.parent.availablePins(selectedOutputPin))
            win.parent = self
            msg = 'Transferring to EditLight UI'
            self._logger.log(msg)
            win.show()

    def __closeBtnAction(self):
        self.close()
        if self.parent is not None:
            self.parent.redrawLightPanel(self.parent.LightControlUI.lights, True)

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, name='', title=''):
        """
        Set the internal logger name and title
        :param name: The backend name of the logger.
        :type name: str
        :param title: The display title of the logger.
        :type title: str
        :return: None
        """
        if name != '':
            self._logger.name = name
        if title != '':
            self._logger.title = title


if __name__ == '__main__':
    pyforms.start_app(LightConfigUI)
