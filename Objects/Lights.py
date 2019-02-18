"""
============
TacOS Lights
============

A passive class that holds an array of configured Light objects
    for the TacOS GUI.

"""

from Objects import Config
from Objects.Logger import Logger
import pickle
from Objects.Light import Light


class Lights(object):

    def __init__(self):
        self._lights = []
        self._logger = Logger('lights', 'Class : Lights')

    def addLight(self, light):
        self._lights.append(light)

    def editLight(self, light, index):
        self._lights[index] = light

    def createLight(self,light):
        self._lights.append(light)

    def rmLight(self, index):
        self._lights.pop(index)

    def save(self):
        configLights = {}
        i = 0
        for x in self.lights:
            configLights[i] = {'name': x.name, 'outputPin': x.outputPin, 'enabled': x.enabled, 'icon': x.icon}
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
            if 'icon' in cfg[key].keys():
                self.addLight(Light(cfg[key]['name'], cfg[key]['outputPin'], cfg[key]['enabled'], cfg[key]['icon']))
            else:
                self.addLight(Light(cfg[key]['name'], cfg[key]['outputPin'], cfg[key]['enabled']))
            i += 1
        lcfg.close()
        msg = 'Loaded %s lights from local config file.' % i
        self._logger.log(msg)

    @property
    def lights(self):
        return self._lights
