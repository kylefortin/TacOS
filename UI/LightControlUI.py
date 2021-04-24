"""
======================
TacOS Light Control UI
======================

Provides a control interface for enabled Light objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from AnyQt.QtGui import QIcon
from Objects import Config, Tools
from Objects.LightControl import LightControl
from Objects.Logger import Logger


class LightControlUI(QWidget):

    def __init__(self, lights, parent):
        super(LightControlUI, self).__init__()
        self.title = 'Light Control UI'
        self.setLayout(QVBoxLayout(self))
        self.lights = lights
        self.parent = parent

        self.logger = Logger('lightControl', "UI : LightControl")

        # Dynamically generate controls
        _keyStrings = []
        for _i, _light in enumerate(self.lights):
            _ctrl = LightControl(_light.name, parent=self, strobe=_light.strobe)
            exec("self._%s = _ctrl" % _i)
            _ctrl.setParent(self)
            _ctrl.setIcon(QIcon(Config.icon('lights', _light.icon)['path']))
            if _light.active:
                _ctrl.setChecked(True)
            _keyStrings.append('_%s' % _i)
        oList = Tools.group(Config.lightColumns, _keyStrings)
        del _keyStrings

        # Dynamically generate panel layout using grouped tuples
        for oTuple in oList:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            for oWidget in oTuple:
                _panel.layout().addWidget(eval('self.%s' % oWidget))
            self.layout().addWidget(_panel)
            del _panel

    def setLight(self, name, state):
        for _light in self.lights:
            if _light.name == name:
                _light.active = state
                self.parent.setOutputPin(_light.outputPin, state)
                break
