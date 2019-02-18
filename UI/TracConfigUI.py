"""
==================================
TacOS TracControl Configuration UI
==================================

Extends the TacOS Tracs class to provide a UI to configure available Trac objects in the TacOS environment.

"""

import pyforms
from Objects.Tracs import Tracs
from Objects.Logger import Logger
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList
from pyforms.controls import ControlButton
from UI.AddTracUI import AddTracUI
from UI.EditTracUI import EditTracUI


class TracConfigUI(Tracs, BaseWidget):

    def __init__(self):
        Tracs.__init__(self)
        BaseWidget.__init__(self, 'TracControl Configuration')

        self._logger = Logger('tracConfig', "UI : TracConfig")

        self._tracsList = ControlList('TracControls',
                                      add_function=self.__createTrac,
                                      remove_function=self.__destroyTrac
                                      )
        self._editBtn = ControlButton('Edit')
        self._closeBtn = ControlButton('Close')

        # Control settings
        self._tracsList.horizontal_headers = ['Name', 'Output Pin', 'Enabled', 'Icon']
        self._tracsList.readonly = True
        self._tracsList.select_entire_row = True

        # Assign button callback fx
        self._editBtn.value = self.__editTrac
        self._closeBtn.value = self.__closeBtnAction
        self.load()

        self.formset = [
            '_tracsList',
            '_editBtn',
            '_closeBtn'
        ]

        msg = 'TacOS TracConfig UI initialized successfully'
        self._logger.log(msg)

    def closeEvent(self, event):
        self.save()
        self._logger.log('Terminating TacOS TracConfig UI')
        self.parent.configBtn.enabled = True

    def addTrac(self, trac):
        super(TracConfigUI, self).addTrac(trac)
        self._tracsList += [trac.name, trac.outputPin, trac.enabled, trac.icon]
        msg = 'Loaded preconfigured Trac : %s, %s, %s, %s' % (
            trac.name,
            trac.outputPin,
            trac.enabled,
            trac.icon
        )
        self._logger.log(msg)

    def editTrac(self, trac, index):
        super(TracConfigUI, self).editTrac(trac, index)
        self._tracsList.set_value(0, index, trac.name)
        self._tracsList.set_value(1, index, trac.outputPin)
        self._tracsList.set_value(2, index, trac.enabled)
        self._tracsList.set_value(3, index, trac.icon)
        trac.close()
        msg = 'Updated Trac at index %s : %s, %s, %s, %s' % (
            index,
            trac.name,
            trac.outputPin,
            trac.enabled,
            trac.icon
        )
        self._logger.log(msg)
        self.updateUI()

    def createTrac(self, trac):
        super(TracConfigUI, self).createTrac(trac)
        self._tracsList += [trac.name, trac.outputPin, trac.enabled, trac.icon]
        self.parent.tracPanel.value = self
        trac.close()
        msg = 'Created new Trac : %s, %s, %s, %s' % (
            trac.name,
            trac.outputPin,
            trac.enabled,
            trac.icon
        )
        self._logger.log(msg)
        self.updateUI()

    def rmTrac(self, index):
        super(TracConfigUI, self).rmTrac(index)
        self._tracsList -= index
        msg = 'Removed Trac at index %s' % (
            index
        )
        self._logger.log(msg)

    def updateUI(self):
        self.close()
        self.parent.redrawTracPanel(self.parent.TracControlUI.tracs)
        win = TracConfigUI()
        win.parent = self.parent
        self.parent.tracPanel.value = win

    def __createTrac(self):
        win = AddTracUI(availablePins=self.parent.availablePins())
        win.parent = self
        msg = 'Transferring to AddTrac UI'
        self._logger.log(msg)
        self.parent.disableConfigButtons()
        self.parent.tracPanel.value = win

    def __destroyTrac(self):
        rows = self._tracsList.selected_rows_indexes
        names = []
        for i in rows:
            names.append(self._tracsList.get_value(0, i))
        for name in names:
            for n in range(self._tracsList.rows_count):
                if self._tracsList.get_value(0, n) == name:
                    self.rmTrac(n)
        self.updateUI()

    def __editTrac(self):
        selectedIndex = self._tracsList.selected_row_index
        if selectedIndex is not None:
            selectedName = self._tracsList.get_value(0, selectedIndex)
            selectedOutputPin = str(self._tracsList.get_value(1, selectedIndex))
            selectedEnabled = self._tracsList.get_value(2, selectedIndex) != 'false'
            selectedIcon = self._tracsList.get_value(3, selectedIndex)
            win = EditTracUI(selectedName, selectedOutputPin, selectedEnabled, selectedIcon,
                             selectedIndex, self.parent.availablePins(selectedOutputPin))
            win.parent = self
            msg = 'Transferring to EditTrac UI'
            self._logger.log(msg)
            self.parent.disableConfigButtons()
            self.parent.tracPanel.value = win

    def __closeBtnAction(self):
        self.close()
        if self.parent is not None:
            self.parent.redrawTracPanel(self.parent.TracControlUI.tracs, True)

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
    pyforms.start_app(TracConfigUI)
