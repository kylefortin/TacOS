"""
==========================
TacOS Light Control Button
==========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from pyforms_gui.controls.control_button import ControlButton
from AnyQt.QtCore import QSize
from Objects import Config


class LightControl(ControlButton):

    def __init__(self, *args, **kwargs):
        super(LightControl, self).__init__(self, *args, **kwargs)
        self._form.clicked.connect(self.__callback)
        self._form.setCheckable(True)
        self._form.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self._form.setFixedSize(Config.controlWidth, Config.controlHeight)

    def __callback(self):
        if self.parent is not None:
            self.parent.setLight(self._label, self._form.isChecked())

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Reject value updates.
        """
        pass

    @property
    def form(self):
        return self._form

