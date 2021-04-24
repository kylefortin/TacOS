"""
===============
TacOS Gyrometer
===============

Custom gyrometer/inclinometer for TacOS environment.

"""

from serial.tools import list_ports

from AnyQt.QtWidgets import QWidget, QHBoxLayout, QLabel
from AnyQt.QtGui import QPixmap, QImage, QTransform, QPainter
from AnyQt.QtCore import QTimer, Qt
from Objects import Config
from Objects.GyroImage import GyroImage
from Objects.SerialMonitor import SerialMonitor


class Gyrometer(QWidget):
    def __init__(self, parent):
        super(Gyrometer, self).__init__()
        self.setLayout(QHBoxLayout(self))
        self.parent = parent
        self.xData = []
        self.yData = []
        self.rotationX = 0
        self.rotationY = 0
        self.comm = None
        self.serial = None

        # Add serial monitor
        comPorts = list_ports.comports()
        for port in comPorts:
            if port.product == "Arduino Uno":
                self.comm = port.device
                break
        if self.comm is not None:
            self.serial = SerialMonitor(port=self.comm, baud=115200)
            self.serial.open()

        # Add serial read timer
        self.serialTimer = QTimer()
        self.serialTimer.timeout.connect(self.__readSerial)

        # Add graphic update timers
        self.sideViewTimer = QTimer()
        self.sideViewTimer.timeout.connect(self.rotateSideView)
        self.frontViewTimer = QTimer()
        self.frontViewTimer.timeout.connect(self.rotateFrontView)

        # Side view icon
        self._sideImage = GyroImage(Config.icons['gyro']['side']['path'], self, 'y',
                                    scaleWidth=150, compassRotation=90, fixedSize=300)
        self.layout().addWidget(self._sideImage)

        # Front view icon
        self._frontImage = GyroImage(Config.icons['gyro']['rear']['path'], self, 'x', scaleHeight=100, fixedSize=300)
        self.layout().addWidget(self._frontImage)

    def __readSerial(self):
        if self.serial is not None:
            data = str(self.serial.readline())
            if "X=" in data:
                if len(self.xData) > 5:
                    n = len(self.xData) - 5
                    del self.xData[:n]
                self.xData.append(float(data.replace("b'X=", "").replace("\\r\\n'", "")))
            elif "Y=" in data:
                if len(self.yData) > 5:
                    n = len(self.yData) - 5
                    del self.yData[:n]
                self.yData.append(float(data.replace("b'Y=", "").replace("\\r\\n'", "")))

    def rotateFrontView(self):
        if len(self.xData) != 0:
            self.rotationX = sum(self.xData) / len(self.xData)
        self._frontImage.repaint()

    def rotateSideView(self):
        if len(self.yData) != 0:
            self.rotationY = sum(self.yData) / len(self.yData)
        self._sideImage.repaint()

    def startSerial(self):
        self.serialTimer.start(50)

    def stopSerial(self):
        self.serialTimer.stop()

    def startRotation(self):
        self.sideViewTimer.start(200)
        self.frontViewTimer.start(200)

    def stopRotation(self):
        self.sideViewTimer.stop()
        self.frontViewTimer.stop()
