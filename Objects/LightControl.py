"""
==========================
TacOS Light Control Button
==========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from AnyQt.QtWidgets import QPushButton
from AnyQt.QtCore import QSize, QTimer
from Objects import Config
import datetime


epoch = datetime.datetime.utcfromtimestamp(0)

def nowMillis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class LightControl(QPushButton):

    def __init__(self, *args, **kwargs):
        self._strobe = kwargs.get('strobe', False)
        self._strobeState = False
        self._strobeTimer = QTimer()
        self._strobeTimer.timeout.connect(self.__strobeEffect)
        self._parent = kwargs.get('parent', None)
        super(LightControl, self).__init__(*args)
        self.clicked.connect(self.__callback)
        self.setCheckable(True)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.controlWidth, Config.controlHeight)
        self._lastPress = 0

    def __callback(self):
        self._strobeTimer.stop()
        if self._parent is not None:
            self._parent.setLight(self.text(), self.isChecked())
            self._strobeState = False
            if self._strobe:
                now = nowMillis(datetime.datetime.now())
                diff = now - self._lastPress
                self._lastPress = now
                if diff <= 500:
                    self.setChecked(True)
                    self._strobeTimer.start(Config.strobeRate/1000)

    def __strobeEffect(self):
        if self._parent is not None:
            self._strobeState = not self._strobeState
            self._parent.setLight(self.text(), self._strobeState)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Reject value updates.
        """
        pass
