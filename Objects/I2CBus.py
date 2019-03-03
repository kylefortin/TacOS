"""
========================
TacOS I2C Bus Controller
========================

Object class for set up communications with the I2C bus on RasPi.

Based on Relay16 by IAScaled.
"""

import time

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

    def __init__(self, bus=1, address=0x20, debug=False):

        # Init logger
        self._logger = Logger('i2cBus', 'I2CBus : Controller')

        # Set debug state
        self._debug = debug

        # Init I2C comms
        if not self._debug:
            self._bus = SMBus(bus)
        else:
            self._bus = None
        self._address = address
        self._state = 0x0000

        # Clear all relays at startup
        self.deEnergizeAll()

    def deEnergizeAll(self):
        self._state = 0x0000
        if not self._debug:
            self._logger.log('De-energizing all relays.')
            success = False
            while not success:
                success = self.__sendI2CData()
                time.sleep(0.1)
        else:
            print('De-energizing all relays.')
            print('I2C Bus state : %s' % str(bin(self._state)))

    def energizeRelay(self, relay):
        """
        Energize relay at position.
        :param relay: The index of the relay to energize (1 - 16)
        :type relay: int
        :return: None
        """
        if checkRelayInputValue(relay):
            self._state |= 1 << (relay - 1)
            if not self._debug:
                self._logger.log('Energizing relay @ position %s' % relay)
                success = False
                while not success:
                    success = self.__sendI2CData()
                    time.sleep(0.1)
            else:
                print('Energizing relay @ position %s' % relay)
                print('I2C Bus state : %s' % str(bin(self._state)))

    def deEnergizeRelay(self, relay):
        """
        De-energize relay at position.
        :param relay: The index of the relay to de-energize (1 - 16)
        :type relay: int
        :return: None
        """
        if checkRelayInputValue(relay):
            self._state &= ~(1 << (relay - 1))
            if not self._debug:
                self._logger.log('De-energizing relay @ position %s' % relay)
                success = False
                while not success:
                    success = self.__sendI2CData()
                    time.sleep(0.1)
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
    def debug(self, value):
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

    @bus.setter
    def bus(self, value):
        """
        Set the I2C bus to use.
        :param value: Bus parameter to set.
        :type value: int
        :return: None
        """
        self._bus = value

    @address.setter
    def address(self, value):
        """
        Set the I2C address to use.
        :param value: I2C address.
        :type value: int
        :return: None
        """
        self._address = value
