import math

from . import *


class TopLevel(Identified):
    def __init__(self) -> None:
        super().__init__()
        self.attachments = URIProperty(self, SBOL_HAS_ATTACHMENT, 0, math.inf)
