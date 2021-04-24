"""
=====================
TacOS Trac Control UI
=====================

Provides a control interface for enabled Trac objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from AnyQt.QtGui import QIcon
from Objects import Config, Tools
from Objects.TracControl import TracControl
from Objects.Logger import Logger


class TracControlUI(QWidget):

    def __init__(self, tracs, parent):
        super(TracControlUI, self).__init__()
        self.title = 'Light Configuration'
        self.setLayout(QVBoxLayout(self))
        self.tracs = tracs
        self.parent = parent

        # Init logger
        self.logger = Logger('tracControl', "UI : TracControl")

        # Dynamically generate controls
        _keyStrings = []
        for _i,_trac in enumerate(self.tracs):
            _ctrl = TracControl(_trac.name, parent=self)
            exec("self._%s = _ctrl" % _i)
            _ctrl.setParent(self)
            _ctrl.setIcon(QIcon(Config.icon('tracControl', _trac.icon)['path']))
            if _trac.active:
                _ctrl.setChecked(True)
            _keyStrings.append('_%s' % _i)
        oList = Tools.group(Config.tracColumns, _keyStrings)
        del _keyStrings

        # Dynamically generate panel layout using grouped tuples
        for oTuple in oList:
            _panel = QWidget(self)
            _panel.setLayout(QHBoxLayout(_panel))
            for oWidget in oTuple:
                _panel.layout().addWidget(eval('self.%s' % oWidget))
            self.layout().addWidget(_panel)
            del _panel

    def setTrac(self, name, state):
        for _trac in self.tracs:
            if _trac.name == name:
                _trac.active = state
                self.parent.setOutputPin(_trac.outputPin, state)
                break
