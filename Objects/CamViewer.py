"""
===============
TacOS CamViewer
===============

Built-in USB webcam viewer for the TacOS environment.

"""

import cv2
import time
from Objects import Config
from Objects.ImageLabel import ImageLabel
from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel
from AnyQt.QtGui import QImage, QPixmap
from AnyQt.QtCore import QTimer, Qt


class CamViewer(QWidget):

    def __init__(self, *args):
        super(CamViewer, self).__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self.nextFrameSlot)
        self._frameRate = Config.camFrameRate
        self._image = QImage()
        self._cap = cv2.VideoCapture(*args)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._image.width())
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._image.height())
        self._cap.set(cv2.CAP_PROP_FPS, Config.camFrameRate)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._isImageFullscreen = False
        self._fullScreenImage = None
        self._page = ImageLabel(self)
        self._page.setAlignment(Qt.AlignCenter)
        self._page.setMaximumHeight(Config.camHeight)
        self._page.mReleased.connect(self.fullscreen)
        self.layout.addWidget(self._page)
        self._frameLabel = QLabel()
        self._frameLabel.setAlignment(Qt.AlignCenter)
        self._time = int(round(time.time() * 1000))
        self.layout.addWidget(self._frameLabel)

    def fullscreen(self):
        if not self.isImageFullscreen:
            cam = QMainWindow(self)
            panel = QWidget(cam)
            panel.layout = QHBoxLayout(panel)
            panel.setLayout(panel.layout)
            image = ImageLabel(panel)
            image.setAlignment(Qt.AlignCenter)
            image.setObjectName("image")
            image.mReleased.connect(cam.parent().fullscreen)
            image.setPixmap(QPixmap.fromImage(cam.parent().image))
            panel.layout.addWidget(image)
            cam.setCentralWidget(panel)
            cam.showFullScreen()
            cam.parent().isImageFullscreen = True
            cam.parent().fullScreenImage = cam
        else:
            self.fullScreenImage.close()
            self.fullScreenImage = None
            self.isImageFullscreen = False

    def nextFrameSlot(self):
        t = int(round(time.time() * 1000))
        ret, f = self.cap.read()
        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        qFormat = QImage.Format_Indexed8
        if len(f.shape) == 3:
            if f.shape[2] == 4:
                qFormat = QImage.Format_RGBA8888
            else:
                qFormat = QImage.Format_RGB888
        self.image = QImage(f, f.shape[1], f.shape[0], f.strides[0], qFormat)
        if self.fullScreenImage is not None:
            img = self.fullScreenImage.findChild(ImageLabel, "image")
            img.setPixmap(QPixmap.fromImage(self.image.scaledToHeight(img.height() * 0.95)))
        else:
            self._page.setPixmap(QPixmap.fromImage(self.image.scaledToHeight(Config.camHeight)))
        self._frameLabel.setText("FPS: " + str(int(1000 / (t - self._time))))
        self._time = t

    def start(self):
        self.timer.start(1000.0 / self.frameRate)
        self._page.repaint()

    def stop(self):
        self.timer.stop()
        self.cap.release()

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
    def timer(self):
        return self._timer

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if not isinstance(value, QImage):
            raise TypeError('Supplied value is not of type (QImage): %s' % type(value).__name__)
        else:
            self._image = value

    @property
    def isImageFullscreen(self):
        return self._isImageFullscreen

    @isImageFullscreen.setter
    def isImageFullscreen(self, value):
        if not isinstance(value, bool):
            raise TypeError('Supplied value is not of type (bool): %s' % type(value).__name__)
        else:
            self._isImageFullscreen = value

    @property
    def fullScreenImage(self):
        return self._fullScreenImage

    @fullScreenImage.setter
    def fullScreenImage(self, value):
        if not isinstance(value, QMainWindow) and not isinstance(value, type(None)):
            raise TypeError('Supplied value is not of type (QMainWindow): %s' % type(value).__name__)
        else:
            self._fullScreenImage = value

    @property
    def stopped(self):
        return self._stopped

    @stopped.setter
    def stopped(self, value):
        if not isinstance(value, bool):
            raise TypeError('Supplied value is not of type (bool): %s' % type(value).__name__)
        else:
            self._stopped = value
