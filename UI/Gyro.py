"""
===============
TacOS Gyrometer
===============

Custom gyrometer/inclinometer for TacOS environment.

"""

from serial.tools import list_ports
import pickle
from AnyQt.QtWidgets import QWidget, QHBoxLayout
from AnyQt.QtCore import QTimer
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
        self.calibrationX = 0
        self.calibrationY = 0
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
                                    scaleWidth=150, compassRotation=90, fixedSize=200)
        self.layout().addWidget(self._sideImage)
        # Front view icon
        self._frontImage = GyroImage(Config.icons['gyro']['rear']['path'], self, 'x',
                                     scaleHeight=100, fixedSize=200)
        self.layout().addWidget(self._frontImage)
        # Load cal values
        with open(Config.cal, 'rb') as file:
            cal = pickle.load(file)
            self.calibrationX = cal['x']
            self.calibrationY = cal['y']

    def __readSerial(self):
        if self.serial is not None:
            data = str(self.serial.readline())
            print(data)
            for s in ["b'", "\\r\\n'"]:
                data = data.replace(s, "")
            print(data)
            if "X=" in data:
                if len(self.xData) > 5:
                    n = len(self.xData) - 5
                    del self.xData[:n]
                self.xData.append(float(data.split('|')[2].replace("X=", "")))
            if "Y=" in data:
                if len(self.yData) > 5:
                    n = len(self.yData) - 5
                    del self.yData[:n]
                self.yData.append(float(data.split('|')[3].replace("Y=", "")))

    def rotateFrontView(self):
        if len(self.xData) != 0:
            self.rotationX = (sum(self.xData) / len(self.xData)) - self.calibrationX
        self._frontImage.repaint()

    def rotateSideView(self):
        if len(self.yData) != 0:
            self.rotationY = (sum(self.yData) / len(self.yData)) - self.calibrationY
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

    def calibrate(self):
        self.calibrationX = sum(self.xData) / len(self.xData) if len(self.xData) > 0 else 0
        self.calibrationY = sum(self.yData) / len(self.yData) if len(self.yData) > 0 else 0
        file = open(Config.cal, 'wb')
        pickle.dump({'x': self.calibrationX, 'y': self.calibrationY}, file)
        file.close()
