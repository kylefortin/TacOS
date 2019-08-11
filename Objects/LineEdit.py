from AnyQt.QtWidgets import QLineEdit
from AnyQt.QtCore import pyqtSignal

class LineEdit(QLineEdit):
    kb = pyqtSignal()

    def __init__(self, *args):
        super(LineEdit, self).__init__(*args)

    def mousePressEvent(self, QMouseEvent):
        super(LineEdit, self).mousePressEvent(QMouseEvent)
        self.kb.emit()

    def focusOutEvent(self, event):
        super(LineEdit, self).focusOutEvent(event)
        if self.parent().focusWidget() != self:
            self.window().dock.hide()
            self.window().osk.rWidget = None
