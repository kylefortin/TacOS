"""
===================
TacOS Cam Viewer UI
===================

Provides a control interface for enabled CamViewer objects in the TacOS environment.

"""

from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from AnyQt.QtCore import Qt
from Objects import Config
from Objects.CamViewer import CamViewer
from Objects.Logger import Logger


class CamViewerUI(QWidget):

    def __init__(self, parent):
        super(CamViewerUI, self).__init__()
        self.parent = parent
        self._logger = Logger('camViewerUI', 'UI : CamViewer')
        self._viewer = None
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self._cam = QWidget()
        self.cam.layout = QVBoxLayout(self.cam)
        self.cam.setLayout(self.cam.layout)
        self.layout.addWidget(self.cam)
        self.layout.setAlignment(Qt.AlignRight)
        container_btn = QWidget()
        container_btn.setObjectName("btns")
        container_btn.layout = QVBoxLayout(container_btn)
        container_btn.setLayout(container_btn.layout)
        container_btn.layout.setAlignment(Qt.AlignCenter)
        for n in range(Config.maxCamConnections):
            button = QPushButton("%s" % n)
            button.setFixedWidth(30)
            button.setFixedHeight(30)
            button.clicked.connect(lambda state, x=n: self.__switchCam(x))
            container_btn.layout.addWidget(button)
        self.layout.addWidget(container_btn)
        del container_btn, n

    def __switchCam(self, cam: int) -> bool:
        if isinstance(cam, float):
            cam = int(cam)
        elif not isinstance(cam, int):
            raise TypeError("Supplied value must be of type: int.")
        if self.viewer is not None:
            self.viewer.stop()
        self.cam.layout.removeWidget(self.viewer)
        self.viewer = CamViewer(cam)
        self.cam.layout.addWidget(self.viewer)
        if self.viewer.cap.isOpened():
            self.viewer.start()
        return self.viewer.cap.isOpened()

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def viewer(self) -> CamViewer:
        return self._viewer

    @viewer.setter
    def viewer(self, viewer: CamViewer) -> None:
        if not isinstance(viewer, CamViewer):
            raise TypeError("Supplied value must be of type: CamViewer.")
        else:
            self._viewer = viewer

    @property
    def cam(self) -> QWidget:
        return self._cam
