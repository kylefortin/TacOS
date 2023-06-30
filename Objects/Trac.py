"""
========================
TacOS TracControl Object
========================

Definition of the traction control object within TacOS.

"""

from Objects.Object import Object


class Trac(Object):

    def __init__(self, **kwargs):
        super(Trac, self).__init__(**kwargs)
