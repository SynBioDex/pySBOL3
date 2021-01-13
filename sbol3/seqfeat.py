import math

from . import *
# Feature is not exported
from .feature import Feature
from .location import Location
from .typing import *


class SequenceFeature(Feature):

    def __init__(self, locations: List[Location],
                 *, identity: str = None,
                 type_uri: str = SBOL_SEQUENCE_FEATURE) -> None:
        super().__init__(identity, type_uri)
        self.locations: oo_list = OwnedObject(self, SBOL_LOCATION,
                                              1, math.inf,
                                              type_constraint=Location,
                                              initial_value=locations)
        self.validate()

    def validate(self):
        super().validate()
        if len(self.locations) < 1:
            raise ValidationError('LocalSubComponent must have at least 1 location')


def build_sequence_feature(identity: str,
                           *, type_uri: str = SBOL_SEQUENCE_FEATURE) -> SBOLObject:
    obj = SequenceFeature([EntireSequence()], identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_LOCATION] = []
    return obj


Document.register_builder(SBOL_SEQUENCE_FEATURE, build_sequence_feature)
