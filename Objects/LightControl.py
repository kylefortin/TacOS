"""
==========================
TacOS Light Control Button
==========================

Custom override for PyQT ControlButton to add function to click() event.

"""


from AnyQt.QtWidgets import QPushButton, QWidget
from AnyQt.QtCore import QSize, QTimer
from Objects import Config
from Objects.Light import Light
from datetime import datetime


epoch = datetime.utcfromtimestamp(0)


def nowMillis():
    return (datetime.now() - epoch).total_seconds() * 1000.0


class LightControl(QPushButton):

    def __init__(self, light: Light, **kwargs):
        self._light = light
        self._lastPress = 0
        self._strobeState = False
        self._strobeTimer = QTimer()
        self._strobeTimer.stop()
        self._strobeTimer.timeout.connect(self.__strobeEffect)
        self._parent = kwargs.get('parent', None)
        super(LightControl, self).__init__(self.light.name)
        self.clicked.connect(self.__callback)
        self.setCheckable(True)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.controlWidth, Config.controlHeight)

    def __callback(self):
        if self.strobeTimer.isActive():
            self.strobeTimer.stop()
        if self.parent is not None:
            self.parent.setLight(self.text(), self.isChecked())
            self.strobeState = False
            if self.light.strobe:
                if nowMillis() - self.lastPress <= 500:
                    self.setChecked(True)
                    self.strobeTimer.start(Config.strobeRate/1000)
                self.lastPress = nowMillis()

    def __strobeEffect(self):
        if self.parent is not None:
            self.strobeState = not self.strobeState
            self.parent.setLight(self.text(), self.strobeState)

    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, light: Light):
        if not (isinstance(light, Light)):
            raise TypeError("Supplied value must of type: Light.")
        else:
            self._light = light

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
    def strobeTimer(self):
        return self._strobeTimer

    @strobeTimer.setter
    def strobeTimer(self, timer: QTimer):
        if not (isinstance(timer, QTimer)):
            raise TypeError("Supplied value must be of type: QTimer.")
        else:
            self._strobeTimer = timer

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: QWidget):
        self._parent = parent

    @property
    def strobeState(self):
        return self._strobeState

    @strobeState.setter
    def strobeState(self, state: bool):
        if not (isinstance(state, bool)):
            raise TypeError("Supplied value must be of type: bool.")
        else:
            self._strobeState = state

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        pass
