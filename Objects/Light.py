"""
===========
TacOS Light
===========

Definition of the light object within TacOS.
"""

from Objects import Config


class Light(object):

    def __init__(self, **kwargs):
        self.name = str(kwargs.get('name', ''))
        self.outputPin = int(kwargs.get('outputPin', 0))
        self.enabled = bool(kwargs.get('enabled', True))
        self.icon = kwargs.get('icon', Config.faIcon('lightbulb'))
        self.strobe = bool(kwargs.get('strobe', False))
        self.active = bool(kwargs.get('active', False))

    @property
    def getInfo(self):
        return {'name': self.name, 'outputPin': self.outputPin, 'enabled': self.enabled, 'icon' : self.icon,
                'active': self.active}
