"""
=========================
TacOS Trac Control Button
=========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from AnyQt.QtWidgets import QPushButton, QWidget
from AnyQt.QtCore import QSize
from Objects import Config
from Objects.Trac import Trac


class TracControl(QPushButton):

    def __init__(self, trac: Trac, **kwargs):
        self._trac = trac
        self._parent = kwargs.get('parent', None)
        super(TracControl, self).__init__(self.trac.name)
        self.clicked.connect(self.__callback)
        self.setCheckable(True)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.controlWidth, Config.controlHeight)

    def __callback(self):
        if self.parent is not None:
            self.parent.setTrac(self.trac, self.isChecked())

    @property
    def trac(self):
        return self._trac

    @trac.setter
    def trac(self, trac: Trac):
        if not (isinstance(trac, Trac)):
            raise TypeError("Supplied value must be of type: Trac.")
        else:
            self._trac = trac

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: QWidget):
        self._parent = parent

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Reject value updates.
        """
        pass
