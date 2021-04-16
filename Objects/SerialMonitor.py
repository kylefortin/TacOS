"""
====================
TacOS Serial Monitor
====================

Extensible serial monitor for the TacOS environment.

"""

import serial


class SerialMonitor(serial.Serial):
    def __init__(self, port, baud):
        super(SerialMonitor, self).__init__()
        self.port = port
        self.baudrate = baud