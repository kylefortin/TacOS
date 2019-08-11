"""
===========================
TacOS OnScreen Keyboard Key
===========================

Built-in OSK Key for the TacOS environment.

"""

from AnyQt.QtWidgets import QPushButton
from AnyQt.QtCore import pyqtSignal


class OSKKey(QPushButton):

    def __init__(self, *args, parent=None):
        super(OSKKey, self).__init__(*args)
        self.setFixedWidth(60)
        self.setFixedHeight(30)
        self._rKey = self.text()

        def btnClick():
            if self._parent is not None:
                self._parent.onClick(self.rKey)

        self._parent = parent
        self.clicked.connect(btnClick)

    @property
    def rKey(self):
        return self._rKey

    @rKey.setter
    def rKey(self, value):
        self._rKey = str(value)
