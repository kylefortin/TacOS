"""
========================
TacOS TracControl Object
========================

Definition of the traction control object within TacOS.

"""

from Objects import Config


class Trac(object):

    def __init__(self, name, outputPin, enabled, icon=Config.icon('tracControl', 'rearDiff')):
        self._name = str(name)
        self._outputPin = int(outputPin)
        self._enabled = bool(enabled)
        self._icon = icon

    @property
    def getInfo(self):
        return {'name': self._name, 'outputPin': self._outputPin, 'enabled': self._enabled, 'icon' : self._icon}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the display name for the Trac object.
        :param value: Name to set.
        :type value: str
        :return: None
        """
        if value != '':
            self._name = value
        elif not isinstance(value, str):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        else:
            raise ValueError('Value must be supplied for Trac name.')

    @property
    def outputPin(self):
        return self._outputPin

    @outputPin.setter
    def outputPin(self, value):
        """
        Set the output pin for the Trac object.
        :param value: Pin to set.
        :type value: int
        :return: None
        """
        if value != None:
            self._name = value
        elif not isinstance(value, int):
            raise TypeError('Value param must be type <int>, given %s' % type(value))
        else:
            raise ValueError('Value must be supplied for Trac name.')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """
        Set the enabled state for the Trac object.
        :param value: State to set.
        :type value: bool
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError('Value param must be type <bool>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for Trac name.')
        else:
            self._enabled = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        """
        Set the icon for the Trac object.
        :param value: Icon to set.
        :type value: str
        :return: None
        """
        if not isinstance(value, str):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for Trac name.')
        else:
            self._icon = value
