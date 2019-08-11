"""
=========================
TacOS Trac Control Button
=========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from AnyQt.QtWidgets import QPushButton
from AnyQt.QtCore import QSize
from Objects import Config


class TracControl(QPushButton):

    def __init__(self, *args, **kwargs):
        self._parent = kwargs.get('parent', None)
        super(TracControl, self).__init__(*args, **kwargs)
        self.clicked.connect(self.__callback)
        self.setCheckable(True)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.controlWidth, Config.controlHeight)

    def __callback(self):
        if self._parent is not None:
            self._parent.setTrac(self.text(), self.isChecked())

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Reject value updates.
        """
        pass
