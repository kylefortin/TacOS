"""
==========================
TacOS OBA Configuration UI
==========================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

import pyforms
from Objects.OBAs import OBAs
from Objects.Logger import Logger
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList
from pyforms.controls import ControlButton
from UI.AddOBAUI import AddOBAUI
from UI.EditOBAUI import EditOBAUI


class OBAConfigUI(OBAs, BaseWidget):

    def __init__(self):
        OBAs.__init__(self)
        BaseWidget.__init__(self, 'OnBoard Air Configuration')

        self._logger = Logger('obaConfig', "UI : OBAConfig")

        self._obaList = ControlList('OBA Elements',
                                    add_function=self.__createOBA,
                                    remove_function=self.__destroyOBA
                                    )
        self._editBtn = ControlButton('Edit')
        self._closeBtn = ControlButton('Close')

        # Control settings
        self._obaList.horizontal_headers = ['Name', 'Output Pin', 'Momentary', 'Enabled', 'Icon']
        self._obaList.readonly = True
        self._obaList.select_entire_row = True

        # Assign button callback fx
        self._editBtn.value = self.__editOBA
        self._closeBtn.value = self.__closeBtnAction
        self.load()

        self.formset = [
            '_obaList',
            '_editBtn',
            '_closeBtn'
        ]

        msg = 'TacOS OBAConfig UI initialized successfully'
        self._logger.log(msg)

    def closeEvent(self, event):
        self.save()
        self._logger.log('Terminating TacOS OBAConfig UI')

    def addOBA(self, oba):
        super(OBAConfigUI, self).addOBA(oba)
        self._obaList += [oba.name, oba.outputPin, oba.momentary, oba.enabled, oba.icon]
        msg = 'Loaded preconfigured OBA Element : %s, %s, %s, %s, %s' % (
            oba.name,
            oba.outputPin,
            oba.momentary,
            oba.enabled,
            oba.icon
        )
        self._logger.log(msg)

    def editOBA(self, oba, index):
        super(OBAConfigUI, self).editOBA(oba, index)
        self._obaList.set_value(0, index, oba.name)
        self._obaList.set_value(1, index, oba.outputPin)
        self._obaList.set_value(2, index, oba.momentary)
        self._obaList.set_value(3, index, oba.enabled)
        self._obaList.set_value(4, index, oba.icon)
        oba.close()
        msg = 'Updated OBA Element at index %s : %s, %s, %s, %s, %s' % (
            index,
            oba.name,
            oba.outputPin,
            oba.momentary,
            oba.enabled,
            oba.icon
        )
        self._logger.log(msg)
        self.updateUI()

    def createOBA(self, oba):
        super(OBAConfigUI, self).createOBA(oba)
        self._obaList += [oba.name, oba.outputPin, oba.enabled, oba.icon]
        oba.close()
        msg = 'Created new OBA Element : %s, %s, %s, %s, %s' % (
            oba.name,
            oba.outputPin,
            oba.enabled,
            oba.momentary,
            oba.icon
        )
        self._logger.log(msg)
        self.updateUI()

    def rmOBA(self, index):
        super(OBAConfigUI, self).rmOBA(index)
        self._obaList -= index
        msg = 'Removed OBA Element at index %s' % (
            index
        )
        self._logger.log(msg)

    def updateUI(self):
        self.close()
        self.parent.redrawOBAPanel(self.parent.OBAControlUI.obas)
        win = OBAConfigUI()
        win.parent = self.parent
        self.parent.obaPanel.value = win

    def __createOBA(self):
        win = AddOBAUI(self.parent.availablePins())
        win.parent = self
        msg = 'Transferring to AddOBA UI'
        self._logger.log(msg)
        self.parent.disableConfigButtons()
        self.parent.obaPanel.value = win

    def __destroyOBA(self):
        rows = self._obaList.selected_rows_indexes
        names = []
        for i in rows:
            names.append(self._obaList.get_value(0, i))
        for name in names:
            for n in range(self._obaList.rows_count):
                if self._obaList.get_value(0, n) == name:
                    self.rmOBA(n)
        self.updateUI()

    def __editOBA(self):
        selectedIndex = self._obaList.selected_row_index
        if selectedIndex is not None:
            selectedIndex = self._obaList.selected_row_index
            selectedName = self._obaList.get_value(0, selectedIndex)
            selectedOutputPin = str(self._obaList.get_value(1, selectedIndex))
            selectedMomentary = self._obaList.get_value(2, selectedIndex) != 'false'
            selectedEnabled = self._obaList.get_value(3, selectedIndex) != 'false'
            selectedIcon = self._obaList.get_value(4, selectedIndex)
            win = EditOBAUI(selectedName, selectedOutputPin, selectedEnabled, selectedIcon,
                            selectedMomentary, selectedIndex, self.parent.availablePins(selectedOutputPin))
            win.parent = self
            msg = 'Transferring to EditOBA UI'
            self._logger.log(msg)
            self.parent.disableConfigButtons()
            self.parent.obaPanel.value = win

    def __closeBtnAction(self):
        self.close()
        if self.parent is not None:
            self.parent.redrawOBAPanel(self.parent.OBAControlUI.obas, True)

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
    pyforms.start_app(OBAConfigUI)
