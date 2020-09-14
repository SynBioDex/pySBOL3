import math

from . import *
# Feature is not exported
from .feature import Feature
from .typing import *


class LocalSubComponent(Feature):

    def __init__(self, types: List[str],
                 *, name: str = None,
                 type_uri: str = SBOL_LOCAL_SUBCOMPONENT) -> None:
        super().__init__(name, type_uri)
        self.types: uri_list = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                           initial_value=types)
        self.locations = OwnedObject(self, SBOL_LOCATION, 0, math.inf)
        self.validate()

    def validate(self):
        super().validate()
        if len(self.types) < 1:
            raise ValidationError('LocalSubComponent must have at least 1 type')


def build_local_subcomponent(name: str,
                             *, type_uri: str = SBOL_LOCAL_SUBCOMPONENT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = LocalSubComponent([missing], name=name, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_TYPE] = []
    return obj


Document.register_builder(SBOL_LOCAL_SUBCOMPONENT, build_local_subcomponent)
