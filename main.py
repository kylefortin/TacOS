#!/usr/bin/env python3

import sys
from AnyQt.QtWidgets import QApplication
from UI.MainWindowUI import MainWindow

app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
