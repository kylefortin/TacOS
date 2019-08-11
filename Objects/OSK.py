"""
=======================
TacOS OnScreen Keyboard
=======================

Built-in OSK for the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from AnyQt.QtCore import Qt
from Objects.OSKKey import OSKKey


class OSK(QWidget):

    def __init__(self, rWidget=None):
        super(OSK, self).__init__()
        self._rWidget = rWidget
        self.layout = QVBoxLayout(self)
        keyLayout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]
        for l in keyLayout:
            panel = QWidget(self)
            panel.layout = QHBoxLayout(panel)
            for key in l:
                button = OSKKey(key, self, parent=self)
                panel.layout.addWidget(button)
            self.layout.addWidget(panel)
        contolPanel = QWidget(self)
        contolPanel.layout = QHBoxLayout(contolPanel)
        self._shift = QPushButton('Shift', self)
        self._shift.setCheckable(True)
        self._shift.setFixedWidth(150)
        contolPanel.layout.addWidget(self._shift)
        spaceBar = OSKKey('space', self, parent=self)
        spaceBar.rKey = ' '
        spaceBar.setFixedWidth(2*self.window().geometry().width()/3)
        contolPanel.layout.addWidget(spaceBar)
        bkspc = OSKKey('delete', self, parent=self)
        bkspc.rKey = '<<'
        contolPanel.layout.addWidget(bkspc)
        self.layout.addWidget(contolPanel)

    def onClick(self, key):
        if self.rWidget is not None:
            if key == '<<':
                self.rWidget.setText(self.rWidget.text()[:-1])
            elif self._shift.isChecked():
                self.rWidget.setText(self.rWidget.text() + key.upper())
                self._shift.setChecked(False)
            else:
                self.rWidget.setText(self.rWidget.text() + key)

    @property
    def rWidget(self):
        return self._rWidget

    @rWidget.setter
    def rWidget(self, value):
        if not isinstance(value, QWidget) and value is not None:
            raise TypeError("Supplied return Widget is not of type QWidget: %s" % type(value).__name__)
        else:
            self._rWidget = value
