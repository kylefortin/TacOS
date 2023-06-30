"""
=================
TacOS OBA Element
=================

Definition of the OBA object within the TacOS environment.

"""

from Objects.Object import Object


class OBA(Object):

    def __init__(self, **kwargs):
        self.momentary = bool(kwargs.get('momentary', False))
        super(OBA, self).__init__(**kwargs)

    @property
    def info(self):
        return {'name': self.name, 'outputPin': self.outputPin, 'enabled': self.enabled, 'icon': self.icon,
                'momentary': self.momentary, 'active': self.active}
