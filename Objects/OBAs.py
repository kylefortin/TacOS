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
        self._obas.append(oba)

    def editOBA(self, oba, index):
        self._obas[index] = oba

    def createOBA(self, oba):
        self._obas.append(oba)

    def rmOBA(self, index):
        self._obas.pop(index)

    def save(self):
        configOBAs = {}
        i = 0
        for x in self.obas:
            configOBAs[i] = {'name': x.name, 'outputPin': x.outputPin, 'momentary': x.momentary,
                             'enabled': x.enabled, 'icon': x.icon}
            i += 1
        obacfg = open(Config.obaConfig, 'wb')
        pickle.dump(configOBAs, obacfg)
        obacfg.close()
        msg = 'Pickled %s OBA elements to local config file.' % i
        self._logger.log(msg)

    def load(self):
        i = 0
        obacfg = open(Config.obaConfig, 'rb')
        cfg = pickle.load(obacfg)
        for key in cfg.keys():
            if 'momentary' in cfg[key].keys():
                self.addOBA(
                    OBA(cfg[key]['name'], cfg[key]['outputPin'], cfg[key]['enabled'],
                        cfg[key]['icon'], cfg[key]['momentary'])
                )
            else:
                self.addOBA(
                    OBA(cfg[key]['name'], cfg[key]['outputPin'], cfg[key]['enabled'],
                        cfg[key]['icon'])
                )
            i += 1
        obacfg.close()
        msg = 'Loaded %s OBA elements from local config file.' % i
        self._logger.log(msg)

    @property
    def obas(self):
        return self._obas
