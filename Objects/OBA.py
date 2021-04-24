"""
=================
TacOS OBA Element
=================

Definition of the OBA object within the TacOS environment.

"""

from Objects import Config


class OBA(object):

    def __init__(self, **kwargs):
        self.name = str(kwargs.get('name', ''))
        self.outputPin = int(kwargs.get('outputPin', 0))
        self.enabled = bool(kwargs.get('enabled', True))
        self.icon = kwargs.get('icon', Config.faIcon('wind'))
        self.momentary = bool(kwargs.get('momentary', False))
        self.active = bool(kwargs.get('active', False))
