import math

from . import *


class Component(TopLevel):

    def __init__(self) -> None:
        super().__init__()
        self.roles = URIProperty(self, SBOL_ROLE, 0, math.inf)
        self.types = URIProperty(self, SBOL_TYPE, 0, math.inf)
        self.sequences = URIProperty(self, SBOL_SEQUENCES, 0, math.inf)
        self.models = URIProperty(self, SBOL_MODELS, 0, math.inf)
