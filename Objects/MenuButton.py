"""
=================
TacOS Menu Button
=================

Custom override for QPushButton used for TacOS sidebar menu.

"""


from AnyQt.QtWidgets import QPushButton
from AnyQt.QtCore import QSize
from Objects import Config


class MenuButton(QPushButton):

    def __init__(self, *args, **kwargs):
        self._panel = kwargs.get('panel', None)
        self._parent = kwargs.get('parent', None)
        super(MenuButton, self).__init__(*args)
        self.clicked.connect(self.__callback)
        self.setCheckable(False)
        self.setIconSize(QSize(Config.iconSize, Config.iconSize))
        self.setFixedSize(Config.menuWidth - 15, Config.menuHeight)

    def __callback(self):
        if self._parent is not None:
            self._parent.setUIPanel(self._panel)

    @property
    def panel(self):
        return self._panel

    @panel.setter
    def panel(self, value):
        self._panel = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
