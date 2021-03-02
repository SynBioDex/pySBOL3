import math

from . import *
# Feature is not exported
from .feature import Feature
from .location import Location
from .typing import *


class SequenceFeature(Feature):

    def __init__(self, locations: List[Location],
                 *, roles: List[str] = None, orientation: str = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_SEQUENCE_FEATURE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         roles=roles, orientation=orientation, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.locations: oo_list = OwnedObject(self, SBOL_LOCATION,
                                              1, math.inf,
                                              type_constraint=Location,
                                              initial_value=locations)


def build_sequence_feature(identity: str,
                           *, type_uri: str = SBOL_SEQUENCE_FEATURE) -> SBOLObject:
    obj = SequenceFeature([EntireSequence()], identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_LOCATION] = []
    return obj


Document.register_builder(SBOL_SEQUENCE_FEATURE, build_sequence_feature)
