"""
==================
TacOS Debug Logger
==================

Logs TacOS UI and class debug information by date/time and originator.

parameters:
    name : (string) The static reference name for the logger.
    originator : (string) The object invoking the logger.  Will be logged as the source of the message.

"""

from Objects import Config, Tools


class Logger(object):

    def __init__(self, name, title, **kwargs):
        self._name = name
        self._title = title
        self._level = kwargs.get('level', 'info')

    def log(self, msg):
        if not (self._level == 'debug' and not Tools.loggingLevel()):
            msg = "%s -- %s -- %s\n" % (Tools.now(), self._title, msg)
            logFile = open(Config.logFile, 'a+')
            logFile.write(msg)
            logFile.close()

    @property
    def getInfo(self):
        return {'name': self._name, 'originator': self._title}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=''):
        """
        Set the object name for the logger.
        :param name: The backend name of the logger.
        :type name: str
        :return: None
        """
        if name != '':
            self._name = name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title=''):
        """
        Set the display title for the logger.
        :param title: The display title for the logger.
        :type title: str
        :return: None
        """
        if title != '':
            self._title = title

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value in [0, 'debug']:
            self._level = 'debug'
        elif value in [1, 'info']:
            self._level = 'info'
        else:
            raise ValueError('Invalid logging level supplied: %s' % value)
