import math

from . import *


class Interface(Identified):

    def __init__(self, *, identity: str = None,
                 type_uri: str = SBOL_INTERFACE) -> None:
        super().__init__(identity, type_uri)
        self.input = ReferencedObject(self, SBOL_INPUT, 0, math.inf)
        self.output = ReferencedObject(self, SBOL_OUTPUT, 0, math.inf)
        self.non_directional = ReferencedObject(self, SBOL_NON_DIRECTIONAL, 0, math.inf)
        self.validate()

    def validate(self) -> None:
        super().validate()


def build_interface(identity: str, *, type_uri: str = SBOL_INTERFACE) -> SBOLObject:
    return Interface(identity=identity, type_uri=type_uri)


Document.register_builder(SBOL_INTERFACE, build_interface)
