"""
===============
TacOS Gyrometer
===============

Custom gyrometer/inclinometer for TacOS environment.

"""

from serial.tools import list_ports

from AnyQt.QtWidgets import QWidget, QHBoxLayout
from AnyQt.QtGui import QPixmap, QImage, QTransform, QPainter
from AnyQt.QtCore import QTimer, Qt

from Objects import Config
from Objects.SerialMonitor import SerialMonitor
from Objects.ImageLabel import ImageLabel


class Gyrometer(QWidget):
    def __init__(self, **kwargs):
        parent = kwargs.get("parent", None)
        self.parent = parent
        super(Gyrometer, self).__init__()
        self.layout = QHBoxLayout(self)
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

        # Add graphic update tiemrs
        self.sideViewTimer = QTimer()
        self.sideViewTimer.timeout.connect(self.rotateSideView)
        self.frontViewTimer = QTimer()
        self.frontViewTimer.timeout.connect(self.rotateFrontView)

        # Compass image
        self._compassImage = QImage(Config.icons['gyro']['compass']['path']).scaledToWidth(250)
        self._compassImageRotated = QImage(
            QPixmap(self._compassImage).transformed(QTransform().rotate(90), Qt.SmoothTransformation))

        # Side view icon
        self._sideImage = QImage(Config.icons['gyro']['side']['path']).scaledToWidth(150)
        self._sideImageLabel = ImageLabel()
        self._sideImageLabel.setAlignment(Qt.AlignCenter)
        self._sideImageLabel.setFixedWidth(250)
        self._sideImageLabel.setFixedHeight(250)
        self.layout.addWidget(self._sideImageLabel)

        # Front view icon
        self._frontImage = QImage(Config.icons['gyro']['rear']['path']).scaledToHeight(100)
        self._frontImageLabel = ImageLabel()
        self._frontImageLabel.setAlignment(Qt.AlignCenter)
        self._frontImageLabel.setFixedWidth(250)
        self._frontImageLabel.setFixedHeight(250)
        self.layout.addWidget(self._frontImageLabel)

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

    def __redrawSideView(self):
        sv_pm = QPixmap(250, 250)
        si_pm = QPixmap(self._sideImage).transformed(QTransform().rotate(self.rotationY), Qt.SmoothTransformation)
        compass_pm = QPixmap(self._compassImageRotated)
        sv_painter = QPainter(sv_pm)
        sv_painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        sv_painter.drawPixmap(0, 0, compass_pm)
        x = (250 - si_pm.width()) / 2
        y = (250 - si_pm.height()) / 2
        sv_painter.drawPixmap(x, y, si_pm)
        sv_painter.end()
        self._sideImageLabel.setPixmap(sv_pm)

    def __redrawFrontView(self):
        fv_pm = QPixmap(250, 250)
        fi_pm = QPixmap(self._frontImage).transformed(QTransform().rotate(self.rotationX), Qt.SmoothTransformation)
        compass_pm = QPixmap(self._compassImage)
        fv_painter = QPainter(fv_pm)
        fv_painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        fv_painter.drawPixmap(0, 0, compass_pm)
        x = (250 - fi_pm.width()) / 2
        y = (250 - fi_pm.height()) / 2
        fv_painter.drawPixmap(x, y, fi_pm)
        fv_painter.end()
        self._frontImageLabel.setPixmap(fv_pm)

    def rotateFrontView(self):
        if len(self.xData) != 0:
            self.rotationX = sum(self.xData) / len(self.xData)
        self.__redrawFrontView()

    def rotateSideView(self):
        if len(self.yData) != 0:
            self.rotationY = sum(self.yData) / len(self.yData)
        self.__redrawSideView()

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
