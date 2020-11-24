"""
===========
TacOS Light
===========

Definition of the light object within TacOS.

parameters:
    name : (string) The name of the light to create in the GUI.
    outputPin : (int) The related output pin to control.
    enabled : (bool) The on/off state of the Light object.

"""

from Objects import Config


class Light(object):

    def __init__(self, **kwargs):
        self._name = str(kwargs.get('name', ''))
        self._outputPin = int(kwargs.get('outputPin', 0))
        self._enabled = bool(kwargs.get('enabled', True))
        self._icon = kwargs.get('icon', Config.faIcon('lightbulb'))
        self._strobe = bool(kwargs.get('strobe', False))

    @property
    def getInfo(self):
        return {'name': self._name, 'outputPin': self._outputPin, 'enabled': self._enabled, 'icon' : self._icon}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the display name for the Light object.
        :param value: Name to set.
        :type value: str
        :return: None
        """
        if value != '':
            self._name = value
        elif not isinstance(value, str):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        else:
            raise ValueError('Value must be supplied for Light name.')

    @property
    def outputPin(self):
        return self._outputPin

    @outputPin.setter
    def outputPin(self, value):
        """
        Set the output pin for the Light object.
        :param value: Pin to set.
        :type value: int
        :return: None
        """
        if value != None:
            self._outputPin = value
        elif not isinstance(value, int):
            raise TypeError('Value param must be type <int>, given %s' % type(value))
        else:
            raise ValueError('Value must be supplied for Light name.')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """
        Set the enabled state for the Light object.
        :param value: State to set.
        :type value: bool
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError('Value param must be type <bool>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for Light name.')
        else:
            self._enabled = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        """
        Set the icon for the Light object.
        :param value: Icon to set.
        :type value: str
        :return: None
        """
        if not isinstance(value, str):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for Light name.')
        else:
            self._icon = value

    @property
    def strobe(self):
        return self._strobe

    @strobe.setter
    def strobe(self, value):
        """
        Set the strobe property for the Light object.
        :param value: Whether or not the light should have strobe capability.
        :type value: bool
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError('Value strobe must be type <bool>, given %s' % type(value))
        else:
            self._strobe = value
