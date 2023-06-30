"""
====================
TacOS Main UI Window
====================

The main UI window structure for the TacOS environment.

"""

from AnyQt.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget
from AnyQt.QtCore import Qt
from UI.MainUI import MainUI
from Objects.OSK import OSK
from Objects import Config
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self._dock = QDockWidget(self)
        self._osk = OSK(rWidget=None)
        self._mainUI = MainUI()
        self.title = 'TacOS'
        self.mainUI.setParent(self)
        self.setStyleSheet(open(Config.css, 'rt').read())
        self.setCentralWidget(self.mainUI)
        self.osk.setParent(self.dock)
        self.dock.setTitleBarWidget(QWidget())
        self.dock.setFloating(True)
        self.dock.setGeometry(0, 0, 800, 480)
        self.dock.setWidget(self._osk)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.dock.hide()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(Config.geometry[0], Config.geometry[1], Config.geometry[2], Config.geometry[3])
        if Config.getPref('startMaximized'):
            self.showFullScreen()
        else:
            self.show()

    @property
    def dock(self):
        return self._dock

    @property
    def osk(self):
        return self._osk

    @property
    def mainUI(self):
        return self._mainUI
