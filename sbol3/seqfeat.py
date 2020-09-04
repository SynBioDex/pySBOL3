import math

from . import *
# Feature is not exported
from .feature import Feature
from .location import Location
from .typing import *


class SequenceFeature(Feature):

    def __init__(self, name: str, locations: List[Location],
                 *, type_uri: str = SBOL_SEQUENCE_FEATURE) -> None:
        super().__init__(name, type_uri)
        self.locations = OwnedObject(self, SBOL_LOCATION, 1, math.inf,
                                     initial_value=locations)
        self.validate()

    def validate(self):
        super().validate()
        if len(self.locations) < 1:
            raise ValidationError('LocalSubComponent must have at least 1 location')


def build_sequence_feature(name: str,
                           *, type_uri: str = SBOL_SEQUENCE_FEATURE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = LocalSubComponent(name, [missing], type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_LOCATION] = []
    return obj


Document.register_builder(SBOL_SEQUENCE_FEATURE, build_sequence_feature)
