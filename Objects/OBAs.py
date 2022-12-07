"""
==================
TacOS OBA Elements
============

A passive class that holds an array of configured Light objects
    for the TacOS GUI.

"""

import pickle
from Objects import Config
from Objects.Logger import Logger
from Objects.OBA import OBA


class OBAs(object):

    def __init__(self):
        self._obas = []
        self._logger = Logger('obas', 'Class : OBAs')

    def addOBA(self, oba):
        self.obas.append(oba)

    def editOBA(self, oba, index):
        self.obas[index] = oba

    def rmOBA(self, index):
        self.obas.pop(index)

    def save(self):
        configOBAs, i = {}, 0
        for _ in self.obas:
            configOBAs[i] = {'name': _.name, 'outputPin': _.outputPin, 'momentary': _.momentary,
                             'enabled': _.enabled, 'icon': _.icon}
            i += 1
        with open(Config.obaConfig, 'wb') as obacfg:
            pickle.dump(configOBAs, obacfg)
        self.logger.log('Pickled %s OBA elements to local config file.' % i)

    def load(self):
        i = 0
        with open(Config.obaConfig, 'rb') as obacfg:
            cfg = pickle.load(obacfg)
            for key in cfg.keys():
                self.addOBA(
                    OBA(
                        name=cfg[key]['name'], outputPin=cfg[key]['outputPin'], enabled=cfg[key]['enabled'],
                        icon=cfg[key]['icon'], momentary=cfg[key]['momentary']
                    )
                )
                i += 1
        self.logger.log('Loaded %s OBA elements from local config file.' % i)

    @property
    def obas(self):
        return self._obas

    @property
    def logger(self):
        return self._logger
