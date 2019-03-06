"""
========================
TacOS OBA Control Button
========================

Custom override for Pyforms ControlButton to add function to click() event.

"""


from pyforms_gui.controls.control_button import ControlButton
from AnyQt.QtCore import QSize
from Objects import Config
import datetime
import pickle

epoch = datetime.datetime.utcfromtimestamp(0)

def nowMillis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class OBAControl(ControlButton):

    def __init__(self, *args, **kwargs):
        momentary = kwargs.get('momentary', False)
        super(OBAControl, self).__init__(self, *args, **kwargs)
        if momentary:
            self._form.setCheckable(False)
            self._form.pressed.connect(self.__onPress)
            self._form.released.connect(self.__onRelease)
        else:
            self._form.clicked.connect(self.__callback)
            self._form.setCheckable(True)
        self._form.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self._form.setFixedSize(Config.controlWidth, Config.controlHeight)
        self._lastPress = 0
        self._block = False

    def __callback(self):
        if self.parent is not None:
            self.parent.setOBA(self._label, self._form.isChecked())

    def __onPress(self):
        if not self._block:
            if self.parent is not None:
                self.parent.setOBA(self._label, True)
        self._block = False
        self._form.setCheckable(False)
        now = nowMillis(datetime.datetime.now())
        diff = now - self._lastPress
        self._lastPress = now
        print(diff)
        if diff <= 1000:
            self._block = True
            self.__doublePress()

    def __onRelease(self):
        if not self._block:
            if self.parent is not None:
                self.parent.setOBA(self._label, False)

    def __doublePress(self):
        self._form.setCheckable(True)
        self._form.setDown(True)
        self._form.update()

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

