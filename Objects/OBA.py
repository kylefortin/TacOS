"""
=================
TacOS OBA Element
=================

Definition of the OBA object within the TacOS environment.

"""

from Objects import Config


class OBA(object):

    def __init__(self, **kwargs):
        self._name = str(kwargs.get('name', ''))
        self._outputPin = int(kwargs.get('outputPin', 0))
        self._enabled = bool(kwargs.get('enabled', True))
        self._icon = kwargs.get('icon', Config.faIcon('wind'))
        self._momentary = bool(kwargs.get('momentary', False))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the display name for the OBA object.
        :param value: Name to set.
        :type value: str
        :return: None
        """
        if value != '':
            self._name = value
        elif not isinstance(value, str):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        else:
            raise ValueError('Value must be supplied for OBA name.')

    @property
    def outputPin(self):
        return self._outputPin

    @outputPin.setter
    def outputPin(self, value):
        """
        Set the output pin for the OBA object.
        :param value: Pin to set.
        :type value: int
        :return: None
        """
        if value is not None:
            self._outputPin = value
        elif not isinstance(value, int):
            raise TypeError('Value param must be type <int>, given %s' % type(value))
        else:
            raise ValueError('Value must be supplied for OBA output pin.')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """
        Set the enabled state for the OBA object.
        :param value: State to set.
        :type value: bool
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError('Value param must be type <bool>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for OBA state.')
        else:
            self._enabled = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        """
        Set the icon for the OBA object.
        :param value: Icon to set.
        :type value: str
        :return: None
        """
        if not isinstance(value, str):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for OBA icon.')
        else:
            self._icon = value

    @property
    def momentary(self):
        return self._momentary

    @momentary.setter
    def momentary(self, value):
        """
        Set the momentary state for the OBA object.
        :param value: State to set.
        :type value: bool
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError('Value param must be type <str>, given %s' % type(value))
        elif value is None:
            raise ValueError('Value must be supplied for OBA momentary action.')
        else:
            self._momentary = value
