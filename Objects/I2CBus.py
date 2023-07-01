"""
========================
TacOS I2C Bus Controller
========================

Object class for set up communications with the I2C bus on RasPi.

Based on Relay16 by IAScaled.
"""

from Objects import Config

try:
    from smbus import SMBus
except ImportError:
    from smbus2 import SMBus

from Objects.Logger import Logger


def checkRelayInputValue(value):
    if value < 1 or value > 16:
        raise ValueError('Relay index %s out of range.  Relay index must be between 1 and 16.' % value)
    elif not isinstance(value, int):
        raise TypeError('Relay index must be of type int (%s supplied).' % type(value))
    else:
        return True


class I2CBus(object):

    def __init__(self, parent):
        # Init logger
        self._logger = Logger('i2cBus', 'I2CBus : Controller')
        self.parent = parent
        # Set debug state
        self._debug = self.parent.prefs.get("i2cDebug", True)
        # Init I2C comms
        if not self.debug:
            self._bus = SMBus(self.parent.prefs.get("i2cBus", Config.defaultI2CBus))
        else:
            self._bus = None
        self._address = self.parent.prefs.get("i2cAddress", Config.defaultI2CAddress)
        self._state = 0x0000
        # Clear all relays at startup
        self.deEnergizeAll()

    def deEnergizeAll(self):
        self.state = 0x0000
        if not self.debug:
            self.logger.log('De-energizing all relays.')
            return self.__sendI2CData()
        else:
            print('De-energizing all relays.')
            print('I2C Bus state : %s' % str(bin(self.state)))

    def energizeRelay(self, relay):
        """
        Energize relay at position.
        :param relay: The index of the relay to energize (1 - 16)
        :type relay: int
        :return: None
        """
        if checkRelayInputValue(relay):
            self.state |= 1 << (relay - 1)
            if not self.debug:
                self.logger.log('Energizing relay @ position %s' % relay)
                return self.__sendI2CData()
            else:
                print('Energizing relay @ position %s' % relay)
                print('I2C Bus state : %s' % str(bin(self.state)))

    def deEnergizeRelay(self, relay):
        """
        De-energize relay at position.
        :param relay: The index of the relay to de-energize (1 - 16)
        :type relay: int
        :return: None
        """
        if checkRelayInputValue(relay):
            self.state &= ~(1 << (relay - 1))
            if not self.debug:
                self.logger.log('De-energizing relay @ position %s' % relay)
                return self.__sendI2CData()
            else:
                print('De-energizing relay @ position %s' % relay)
                print('I2C Bus state : %s' % str(bin(self._state)))

    def __sendI2CData(self):
        try:
            self.bus.write_byte_data(
                int(self.address, 16), 0xFF & ~self.state, 0xFF & (~(0x00FF & (self.state >> 8)))
            )
            return True
        except Exception as e:
            self.logger.log('Error setting relay state : %s' % e)
            return False

    @property
    def logger(self):
        return self._logger

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError('Debug value must be of type bool, %s provided.' % type(value))
        else:
            self._debug = value

    @property
    def bus(self):
        return self._bus

    @property
    def address(self):
        return self._address

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: int):
        self._state = state

    @bus.setter
    def bus(self, value: int):
        """
        Set the I2C bus to use.
        :param value: Bus parameter to set.
        :type value: int
        :return: None
        """
        self._bus = value

    @address.setter
    def address(self, value: str):
        """
        Set the I2C address to use.
        :param value: I2C address.
        :type value: int
        :return: None
        """
        self._address = value
