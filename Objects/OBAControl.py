"""
========================
TacOS OBA Control Button
========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from AnyQt.QtWidgets import QPushButton
from AnyQt.QtCore import QSize
from Objects import Config
import datetime


epoch = datetime.datetime.utcfromtimestamp(0)


def nowMillis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class OBAControl(QPushButton):

    def __init__(self, *args, **kwargs):
        momentary = kwargs.get('momentary', False)
        self._parent = kwargs.get('parent', None)
        super(OBAControl, self).__init__(*args)
        if momentary:
            self.setCheckable(False)
            self.pressed.connect(self.__onPress)
            self.released.connect(self.__onRelease)
        else:
            self.clicked.connect(self.__callback)
            self.setCheckable(True)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.controlWidth, Config.controlHeight)
        self._lastPress = 0
        self._block = False

    def __callback(self):
        if self._parent is not None:
            self._parent.setOBA(self.text(), self.isChecked())

    def __onPress(self):
        if not self._block:
            if self._parent is not None:
                self._parent.setOBA(self.text(), True)
        self._block = False
        self.setCheckable(False)
        now = nowMillis(datetime.datetime.now())
        diff = now - self._lastPress
        self._lastPress = now
        if diff <= 500:
            self._block = True
            self.__doublePress()

    def __onRelease(self):
        if not self._block:
            if self._parent is not None:
                self._parent.setOBA(self.text(), False)

    def __doublePress(self):
        self.setCheckable(True)
        self.setDown(True)
        self.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Reject value updates.
        """
        pass
