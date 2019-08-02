"""
============================
TacOS Light Configuration UI
============================

Extends the TacOS Lights class to provide a UI to configure available Light objects in the TacOS environment.

"""

import pyforms
from Objects.Logger import Logger
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCombo


class CameraConfigUI(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'Camera Configuration')
        self._logger = Logger('cameraConfig', "UI : CameraConfig")
        self._usbList = ControlCombo()

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
