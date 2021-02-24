import math
from typing import List

from . import *


class Interface(Identified):
    """The Interface class is a way of explicitly specifying the interface
    of a Component.

    """

    def __init__(self, *, input: str = None, output: str = None,
                 nondirectional: str = None, name: str = None,
                 description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_INTERFACE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.input = ReferencedObject(self, SBOL_INPUT, 0, math.inf,
                                      initial_value=input)
        self.output = ReferencedObject(self, SBOL_OUTPUT, 0, math.inf,
                                       initial_value=output)
        self.nondirectional = ReferencedObject(self, SBOL_NONDIRECTIONAL,
                                               0, math.inf,
                                               initial_value=nondirectional)


def build_interface(identity: str, *, type_uri: str = SBOL_INTERFACE) -> SBOLObject:
    return Interface(identity=identity, type_uri=type_uri)


Document.register_builder(SBOL_INTERFACE, build_interface)
