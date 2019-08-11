"""
===============
TacOS CamViewer
===============

Built-in USB webcam viewer for the TacOS environment.

"""

import cv2
import sys
from AnyQt.QtWidgets import QWidget, QLabel,\
    QVBoxLayout
from AnyQt.QtGui import QImage, QPixmap
from AnyQt.QtCore import QTimer
from Objects import Config


class CamViewer(QWidget):
    def __init__(self, *args):
        super(CamViewer, self).__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self.nextFrameSlot)
        self._frameRate = 15
        self._cap = cv2.VideoCapture(*args)
        self._cap.set(cv2.CAP_PROP_CONVERT_RGB, True)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self._page = QLabel()
        layout.addWidget(self._page)

    def nextFrameSlot(self):
        ret, f = self.cap.read()
        f = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
        img = QImage(f, f.shape[1], f.shape[0], QImage.Format_Grayscale8)
        self._page.setPixmap(QPixmap.fromImage(img))

    def start(self):
        self.timer.start(1000./self.frameRate)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(CamViewer, self).deleteLater()

    @property
    def frameRate(self):
        return self._frameRate

    @frameRate.setter
    def frameRate(self, value):
        if not isinstance(value, int):
            raise TypeError('Supplied frame rate is not of type (int): %s' % type(value).__name__)
        else:
            self._frameRate = value

    @property
    def cap(self):
        return self._cap

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if not isinstance(value, int):
            raise TypeError('Supplied frame index is not of type (int): %s' % type(value).__name__)
        else:
            self._frame = value

    @property
    def capturing(self):
        return self._capturing

    @property
    def timer(self):
        return self._timer
