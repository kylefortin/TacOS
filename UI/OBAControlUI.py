"""
====================
TacOS OBA Control UI
====================

Provides a control interface for enabled OBA objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from AnyQt.QtGui import QIcon
from Objects import Config, Tools
from Objects.OBAControl import OBAControl
from Objects.Logger import Logger


class OBAControlUI(QWidget):

    def __init__(self, obas, parent):
        super(OBAControlUI, self).__init__()
        self.title = 'OnBoard Air Control UI'
        self.setLayout(QVBoxLayout(self))
        self.obas = obas
        self.parent = parent

        # Init logger
        self.logger = Logger('obaControl', "UI : OBAControl")

        # Dynamically generate controls
        _keyStrings = []
        for _i, _oba in enumerate(self.obas):
            _ctrl = OBAControl(_oba.name, momentary=_oba.momentary, parent=self)
            exec("self._%s = _ctrl" % _i)
            _ctrl.setIcon(QIcon(Config.icon('oba', _oba.icon)['path']))
            if _oba.active:
                _ctrl.setChecked(True)
            _keyStrings.append('_%s' % _i)
        _oList = Tools.group(Config.obaColumns, _keyStrings)
        del _keyStrings

        # Dynamically generate panel layout using grouped tuples
        for oTuple in _oList:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            for oWidget in oTuple:
                _panel.layout().addWidget(eval('self.%s' % oWidget))
            self.layout().addWidget(_panel)
            del _panel

    def setOBA(self, name, state):
        for _oba in self.obas:
            if _oba.name == name:
                _oba.active = state
                self.parent.setOutputPin(_oba.outputPin, state)
                break
