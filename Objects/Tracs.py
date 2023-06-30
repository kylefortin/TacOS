"""
==================
TacOS TracControls
==================

A passive class that holds an array of configured Trac objects for the TacOS GUI.

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
        self.tracs.append(trac)

    def editTrac(self, trac, index):
        self.tracs[index] = trac

    def rmTrac(self, index):
        self.tracs.pop(index)

    def save(self):
        configTracs, i = {}, 0
        for _ in self.tracs:
            configTracs[i] = {'name': _.name, 'outputPin': _.outputPin, 'enabled': _.enabled, 'icon': _.icon}
            i += 1
        with open(Config.tracConfig, 'wb') as tcfg:
            pickle.dump(configTracs, tcfg)
        self.logger.log('Pickled %s tracs to local config file.' % i)
        del configTracs, i, tcfg

    def load(self):
        i = 0
        with open(Config.tracConfig, 'rb') as tcfg:
            cfg = pickle.load(tcfg)
            for key in cfg.keys():
                self.addTrac(
                    Trac(
                        name=cfg[key]['name'], outputPin=cfg[key]['outputPin'], enabled=cfg[key]['enabled'],
                      icon=cfg[key]['icon']
                    )
                )
                i += 1
        self.logger.log('Loaded %s tracs from local config file.' % i)
        del i, cfg, key

    @property
    def tracs(self):
        return self._tracs

    @property
    def logger(self):
        return self._logger
