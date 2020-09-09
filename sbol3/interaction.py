import math
from typing import List

from . import *


class Interaction(Identified):

    def __init__(self, name: str, interaction_type: List[str],
                 *, type_uri: str = SBOL_INTERACTION) -> None:
        super().__init__(name, type_uri)
        self.types = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                 initial_value=interaction_type)
        self.participations = OwnedObject(self, SBOL_PARTICIPATIONS, 0, math.inf)

    def validate(self) -> None:
        super().validate()


def build_interaction(name: str, *, type_uri: str = SBOL_INTERACTION) -> SBOLObject:
    interaction_type = PYSBOL3_MISSING
    obj = Interaction(name, [interaction_type], type_uri=type_uri)
    # Remove the dummy type
    obj._properties[SBOL_TYPE] = []
    return obj


Document.register_builder(SBOL_INTERACTION, build_interaction)
