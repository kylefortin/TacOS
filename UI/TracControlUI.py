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
from Objects.Trac import Trac


class TracControlUI(QWidget):

    def __init__(self, parent):
        super(TracControlUI, self).__init__()
        self.title = 'Light Configuration'
        self.setLayout(QVBoxLayout(self))
        self.parent = parent
        self.tracs = self.parent.tracs

        # Init logger
        self.logger = Logger('tracControl', "UI : TracControl")

        # Dynamically generate controls
        _keyStrings = []
        for _i, _trac in enumerate(self.tracs.tracs):
            _ctrl = TracControl(_trac, parent=self)
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

    def setTrac(self, trac: Trac, state):
        trac.active = self.parent.setOutputPin(trac.outputPin, state)
