from AnyQt.QtWidgets import QLabel
from AnyQt.QtGui import QImage, QPainter, QPixmap, QTransform, QColor
from AnyQt.QtCore import pyqtSignal, Qt
from Objects import Config


class GyroImage(QLabel):
    mReleased = pyqtSignal()

    def __init__(self, path, parent, direction, fixedSize=250, scaleHeight=None, scaleWidth=None, compassRotation=0):
        super(GyroImage, self).__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setFixedWidth(fixedSize)
        self.setFixedHeight(fixedSize)
        self.parent = parent
        self.compassImage = QImage(Config.icons['gyro']['compass']['path']).scaledToWidth(self.width())
        if scaleWidth is not None:
            self.image = QImage(path).scaledToWidth(scaleWidth)
        elif scaleHeight is not None:
            self.image = QImage(path).scaledToHeight(scaleHeight)
        else:
            self.image = QImage(path)
        self.direction = direction
        self.compassRotation = compassRotation

    def paintEvent(self, QPaintEvent):
        import math


        if self.direction == 'x':
            _angle = self.parent.rotationX
            _x1 = self.width() / 2
            _y1 = self.height() / 2
            _x2 = math.cos(math.radians(_angle)) * (self.width() / 2)
            _y2 = math.sin(math.radians(_angle)) * (self.width() / 2)
        elif self.direction == 'y':
            _angle = self.parent.rotationY
            _x1 = self.width() / 2
            _y1 = self.height() / 2
            _x2 = math.cos(math.radians(_angle + 90)) * (self.height() / 2)
            _y2 = math.sin(math.radians(_angle + 90)) * (self.height() / 2)
        else:
            _angle = 0
            _x1 = 0
            _y1 = 0
            _x2 = 0
            _y2 = 0
        _painter = QPainter(self)
        _pm = QPixmap(self.width(), self.height())
        _pm_compass = QPixmap(self.compassImage).transformed(QTransform().rotate(self.compassRotation))
        _pm_image = QPixmap(self.image).transformed(QTransform().rotate(_angle))
        _painter.drawPixmap(0, 0, _pm_compass)
        _painter.setPen(QColor(255, 160, 47))
        _painter.drawLine(_x1, _y1, _x2, _y2)
        _x = (self.width() - _pm_image.width()) / 2
        _y = (self.height() - _pm_image.height()) / 2
        _painter.drawPixmap(_x, _y, _pm_image)

        _painter.end()

    def mouseReleaseEvent(self, QMouseEvent):
        super(QLabel, self).mouseReleaseEvent(QMouseEvent)
        self.mReleased.emit()
