#!/usr/bin/env python3

import pickle
import os
import sys

from pyforms_gui.appmanager import StandAloneContainer, QApplication

from UI.MainUI import MainUI
from Objects import Config


pPrefs = open(Config.prefs, 'rb')
prefs = pickle.load(pPrefs)
pPrefs.close()


def start_app(ClassObject, geometry=None, stylesheet=None):
    from confapp import conf

    app = QApplication(sys.argv)

    conf += 'pyforms_gui.settings'

    mainwindow = StandAloneContainer(ClassObject)

    myapp = mainwindow.centralWidget()

    if geometry is not None:
        mainwindow.show()
        mainwindow.setGeometry(*geometry)
    else:
        mainwindow.showFullScreen()

    if conf.PYFORMS_QUALITY_TESTS_PATH is not None:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--test", help="File with the tests script")
        args = parser.parse_args()

        if args.test:
            TEST_PATH = os.path.join(conf.PYFORMS_QUALITY_TESTS_PATH, args.test)
            TEST_FILE_PATH = os.path.join(TEST_PATH, args.test + '.py')
            DATA_PATH = os.path.join(TEST_PATH, 'data', sys.platform)
            INPUT_DATA_PATH = os.path.join(DATA_PATH, 'input-data')
            OUTPUT_DATA_PATH = os.path.join(DATA_PATH, 'output-data')
            EXPECTED_DATA_PATH = os.path.join(DATA_PATH, 'expected-data')

            with open(TEST_FILE_PATH) as f:
                global_vars = {}  # globals()
                local_vars = locals()
                code = compile(f.read(), TEST_FILE_PATH, 'exec')

                exec(code, global_vars, local_vars)

    if stylesheet:
        app.setStyleSheet(stylesheet)
    app.exec_()
    return myapp


if 'startMaximized' in prefs.keys():
    startMax = prefs['startMaximized']
else:
    startMax = False
if startMax:
    start_app(MainUI)
else:
    start_app(MainUI, geometry=Config.geometry)
