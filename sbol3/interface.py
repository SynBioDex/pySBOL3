import math
from typing import List

from . import *


class Interface(Identified):

    def __init__(self, name: str, *, type_uri: str = SBOL_INTERFACE) -> None:
        super().__init__(name, type_uri)
        self.input = ReferencedObject(self, SBOL_INPUT, 0, math.inf)
        self.output = ReferencedObject(self, SBOL_OUTPUT, 0, math.inf)
        self.non_directional = ReferencedObject(self, SBOL_NON_DIRECTIONAL, 0, math.inf)
        self.validate()

    def validate(self) -> None:
        super().validate()


Document.register_builder(SBOL_INTERFACE, Interface)
