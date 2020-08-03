from . import *


class Identified(SBOLObject):
    def __init__(self) -> None:
        super().__init__()
        self.display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
