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
from Objects.Light import Light


class LightControlUI(QWidget):

    def __init__(self, parent):
        super(LightControlUI, self).__init__()
        self.title = 'Light Control UI'
        self.setLayout(QVBoxLayout(self))
        self.parent = parent
        self.lights = self.parent.lights
        self.logger = Logger('lightControl', "UI : LightControl")
        # Dynamically generate controls
        _keyStrings = []
        for _i, _light in enumerate(self.lights.lights):
            _ctrl = LightControl(_light, parent=self, strobe=_light.strobe)
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

    def setLight(self, light: Light, state):
        light.active = self.parent.setOutputPin(light.outputPin, state)
