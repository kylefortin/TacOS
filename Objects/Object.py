"""
=====================
TacOS Generic Element
=====================

Definition of the generic base object within the TacOS environment.

"""

from Objects import Config


class Object(object):

    def __init__(self, **kwargs):
        self.name = str(kwargs.get('name', ''))
        self.outputPin = int(kwargs.get('outputPin', 0))
        self.enabled = bool(kwargs.get('enabled', True))
        self.icon = kwargs.get('icon', Config.icon('tracControl', 'rearDiff'))
        self.active = kwargs.get('active', False)

    @property
    def info(self):
        return {'name': self.name, 'outputPin': self.outputPin, 'enabled': self.enabled, 'icon': self.icon,
                'active': self.active}
