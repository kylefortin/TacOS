"""
===========
TacOS Light
===========

Definition of the light object within TacOS.
"""

from Objects.Object import Object


class Light(Object):

    def __init__(self, **kwargs):
        self.strobe = bool(kwargs.get('strobe', False))
        super(Light, self).__init__(**kwargs)

    @property
    def info(self):
        return {'name': self.name, 'outputPin': self.outputPin, 'enabled': self.enabled, 'icon': self.icon,
                'strobe': self.strobe, 'active': self.active}
