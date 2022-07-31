"""
=======================
TacOS OnScreen Keyboard
=======================

Built-in OSK for the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from AnyQt.QtCore import Qt
from Objects.OSKKey import OSKKey


class OSK(QWidget):

    def __init__(self, rWidget=None):
        super(OSK, self).__init__()
        self.showFullScreen()
        self._rWidget = rWidget
        self.layout = QVBoxLayout(self)
        self.currentText = QLabel(self)
        self.currentText.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\
                                        padding: 1px;\
                                        border-style: solid;\
                                        border: 1px solid #1e1e1e;\
                                        border-radius: 5;\
                                        selection-background-color: #ffaa00;")
        self.currentText.setAlignment(Qt.AlignCenter)
        if rWidget is not None:
            self.currentText.setText(rWidget.text())
        self.layout.addWidget(self.currentText)
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
        self.closeButton = QPushButton("OK", self)
        self.closeButton.clicked.connect(self.__closeButtonAction)
        self.layout.addWidget(self.closeButton)

    def onClick(self, key):
        if self.rWidget is not None:
            if key == '<<':
                self.rWidget.setText(self.rWidget.text()[:-1])
            elif self._shift.isChecked():
                self.rWidget.setText(self.rWidget.text() + key.upper())
                self._shift.setChecked(False)
            else:
                self.rWidget.setText(self.rWidget.text() + key)
            self.currentText.setText(self.rWidget.text())

    def __closeButtonAction(self):
        self.parent().hide()

    @property
    def rWidget(self):
        return self._rWidget

    @rWidget.setter
    def rWidget(self, value):
        if not isinstance(value, QWidget) and value is not None:
            raise TypeError("Supplied return Widget is not of type QWidget: %s" % type(value).__name__)
        else:
            self._rWidget = value
            self.currentText.setText(value.text())
