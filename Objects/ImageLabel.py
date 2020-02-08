from AnyQt.QtWidgets import QLabel
from AnyQt.QtCore import pyqtSignal


class ImageLabel(QLabel):
    mReleased = pyqtSignal()

    def __init__(self, *args):
        super(ImageLabel, self).__init__(*args)

    def mouseReleaseEvent(self, QMouseEvent):
        super(QLabel, self).mouseReleaseEvent(QMouseEvent)
        self.mReleased.emit()
