"""
==================
TacOS TracControls
==================

A passive class that holds an array of configured Trac objects
    for the TacOS GUI.

"""

import pickle
from Objects import Config
from Objects.Logger import Logger
from Objects.Trac import Trac


class Tracs(object):

    def __init__(self):
        self._tracs = []
        self._logger = Logger('tracs', 'Class : Tracs')

    def addTrac(self, trac):
        self._tracs.append(trac)

    def editTrac(self, trac, index):
        self._tracs[index] = trac

    def createTrac(self, trac):
        self._tracs.append(trac)

    def rmTrac(self, index):
        self._tracs.pop(index)

    def save(self):
        configTracs = {}
        i = 0
        for x in self.tracs:
            configTracs[i] = {'name': x.name, 'outputPin': x.outputPin, 'enabled': x.enabled, 'icon': x.icon}
            i += 1
        tcfg = open(Config.tracConfig, 'wb')
        pickle.dump(configTracs, tcfg)
        tcfg.close()
        msg = 'Pickled %s tracs to local config file.' % i
        self._logger.log(msg)

    def load(self):
        i = 0
        tcfg = open(Config.tracConfig, 'rb')
        cfg = pickle.load(tcfg)
        for key in cfg.keys():
            self.addTrac(Trac(name=cfg[key]['name'], outputPin=cfg[key]['outputPin'], enabled=cfg[key]['enabled'],
                              icon=cfg[key]['icon']))
            i += 1
        tcfg.close()
        msg = 'Loaded %s tracs from local config file.' % i
        self._logger.log(msg)

    @property
    def tracs(self):
        return self._tracs
