"""
============
TacOS Lights
============

A passive class that holds an array of configured Light objects
    for the TacOS GUI.

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
        self._lights.append(light)

    def editLight(self, light, index):
        self._lights[index] = light

    def rmLight(self, index):
        self._lights.pop(index)

    def save(self):
        configLights = {}
        i = 0
        for x in self.lights:
            configLights[i] = {'name': x.name, 'outputPin': x.outputPin, 'enabled': x.enabled, 'icon': x.icon, 'strobe': x.strobe}
            i += 1
        lcfg = open(Config.lightConfig, 'wb')
        pickle.dump(configLights, lcfg)
        lcfg.close()
        msg = 'Pickled %s lights to local config file.' % i
        self._logger.log(msg)

    def load(self):
        i = 0
        lcfg = open(Config.lightConfig, 'rb')
        cfg = pickle.load(lcfg)
        for key in cfg.keys():
            self.addLight(Light(name=cfg[key]['name'], outputPin=cfg[key]['outputPin'], enabled=cfg[key]['enabled'],
                                icon=cfg[key]['icon'], strobe=cfg[key]['strobe']))
            i += 1
        lcfg.close()
        msg = 'Loaded %s lights from local config file.' % i
        self._logger.log(msg)

    @property
    def lights(self):
        return self._lights
