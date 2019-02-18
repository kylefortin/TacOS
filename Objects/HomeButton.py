"""
=====================
TacOS Home Nav Button
=====================

Custom override for Pyforms ControlButton.

"""


from pyforms.controls import ControlButton


class HomeButton(ControlButton):

    def __init__(self, *args, **kwargs):
        super(HomeButton, self).__init__(self, *args, **kwargs)
        self._form.clicked.connect(self.__callback)

    def __callback(self):
        if self.parent is not None:
            self.parent.reload('HomeUI')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Reject value updates.
        """
        pass

