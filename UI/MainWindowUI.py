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
import pickle


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = 'TacOS'
        self._mainUI = MainUI()
        self._mainUI.setParent(self)
        self.setStyleSheet(open(Config.css, 'rt').read())
        self.setCentralWidget(self._mainUI)
        self._dock = QDockWidget(self)
        self._osk = OSK(rWidget=None)
        self._osk.setParent(self._dock)
        self._dock.setTitleBarWidget(QWidget())
        self._dock.setFloating(True)
        self._dock.setGeometry(0, 0, 800, 480)
        self._dock.setWidget(self._osk)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._dock)
        self._dock.hide()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())