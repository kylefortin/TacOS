"""
============
TacOS Lights
============

A passive class that holds an array of configured Light objects for the TacOS GUI.

"""

import pickle
from Objects import Config
from Objects.Logger import Logger
from Objects.Light import Light


class Lights(object):

    def __init__(self):
        self._lights = []
        self._logger = Logger('lights', 'Class : Lights')

    def addLight(self, light):
        self.lights.append(light)

    def editLight(self, light, index):
        self.lights[index] = light

    def rmLight(self, index):
        self.lights.pop(index)

    def save(self):
        configLights, i = {}, 0
        for _ in self.lights:
            configLights[i] = {'name': _.name, 'outputPin': _.outputPin, 'enabled': _.enabled,
                               'icon': _.icon, 'strobe': _.strobe}
            i += 1
        with open(Config.lightConfig, 'wb') as lcfg:
            pickle.dump(configLights, lcfg)
        self.logger.log('Pickled %s lights to local config file.' % i)
        del configLights, i, lcfg

    def load(self):
        i = 0
        with open(Config.lightConfig, 'rb') as lcfg:
            cfg = pickle.load(lcfg)
            for key in cfg.keys():
                self.addLight(
                    Light(
                        name=cfg[key]['name'], outputPin=cfg[key]['outputPin'], enabled=cfg[key]['enabled'],
                        icon=cfg[key]['icon'], strobe=cfg[key]['strobe'])
                )
                i += 1
        self.logger.log('Loaded %s lights from local config file.' % i)
        del i, cfg, key

    @property
    def lights(self):
        return self._lights

    @property
    def logger(self):
        return self._logger