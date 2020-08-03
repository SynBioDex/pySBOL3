import math

from . import *


class Component(TopLevel):

    def __init__(self) -> None:
        super().__init__()
        self.roles = URIProperty(self, SBOL_ROLE, 0, math.inf)
