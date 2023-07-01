"""
========================
TacOS OBA Control Button
========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from AnyQt.QtWidgets import QPushButton, QWidget
from AnyQt.QtCore import QSize
from Objects import Config
from Objects.OBA import OBA
from datetime import datetime


epoch = datetime.utcfromtimestamp(0)


def nowMillis():
    return (datetime.now() - epoch).total_seconds() * 1000.0


class OBAControl(QPushButton):

    def __init__(self, oba: OBA, **kwargs):
        self._oba = oba
        self._parent = kwargs.get('parent', None)
        self._lastPress = 0
        self._block = False
        super(OBAControl, self).__init__(self.oba.name)
        if self._oba.momentary:
            self.setCheckable(False)
            self.pressed.connect(self.__onPress)
            self.released.connect(self.__onRelease)
        else:
            self.clicked.connect(self.__callback)
            self.setCheckable(True)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.controlWidth, Config.controlHeight)

    def __callback(self):
        if self.parent is not None:
            self.parent.setOBA(self.oba, self.isChecked())

    def __onPress(self):
        if not self.block:
            if self.parent is not None:
                self.parent.setOBA(self.oba, True)
        self.block = False
        self.setCheckable(False)
        if nowMillis() - self.lastPress <= 500:
            self.block = True
            self.__doublePress()
        self.lastPress = nowMillis()

    def __onRelease(self):
        if not self.block:
            if self.parent is not None:
                self.parent.setOBA(self.oba, False)

    def __doublePress(self):
        self.setCheckable(True)
        self.setDown(True)
        self.update()

    @property
    def oba(self):
        return self._oba

    @oba.setter
    def oba(self, oba: OBA):
        if not (isinstance(oba, OBA)):
            raise TypeError("Supplied value must be of type: OBA.")
        else:
            self._oba = oba

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: QWidget):
        self._parent = parent

    @property
    def lastPress(self):
        return self._lastPress

    @lastPress.setter
    def lastPress(self, millis: float):
        if not (isinstance(millis, float)):
            raise TypeError("Supplied value must be of type: float.")
        else:
            self._lastPress = millis

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block: bool):
        if not (isinstance(block, bool)):
            raise TypeError("Supplied value must be of type: bool.")
        else:
            self._block = block

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        pass
