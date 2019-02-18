"""
========================
TacOS Icon Control Combo
========================

Custom override for Pyforms ControlCombo.

"""


from pyforms_gui.allcontrols import ControlCombo
from AnyQt.QtGui import QIcon


class IconCombo(ControlCombo):

    def __init__(self, *args, **kwargs):
        super(IconCombo, self).__init__(*args, **kwargs)

    def setItemIcon(self, idx, icon):
        self._combo.setItemIcon(idx, QIcon(icon))

    @property
    def combo(self):
        return self._combo

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        for key in self._items:
            if value == self._items[key]:
                index = self._combo.findText(key)
                self._combo.setCurrentIndex(index)
                if self._value != value:
                    self.changed_event()
                self._value = self._items[key]
