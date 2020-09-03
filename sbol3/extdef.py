import math
from typing import List

from . import *

# Feature is not exported
from .feature import Feature


class ExternallyDefined(Feature):
    """The ExternallyDefined class has been introduced so that
    external definitions in databases like ChEBI or UniProt
    can be referenced.
    """

    def __init__(self, name: str, types: List[str], definition: str,
                 *, type_uri: str = SBOL_EXTERNALLY_DEFINED):
        super().__init__(name, type_uri)
        self.types = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                 initial_value=types)
        self.definition = URIProperty(self, SBOL_DEFINITION, 1, 1,
                                      initial_value=definition)
        self.validate()

    def validate(self):
        if len(self.types) < 1:
            raise ValidationError('ExternallyDefined must contain at least 1 type')
        if self.definition is None:
            raise ValidationError('ExternallyDefined must have a definition')


def build_externally_defined(name: str,
                             *, type_uri: str = SBOL_EXTERNALLY_DEFINED) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = ExternallyDefined(name, [missing], missing, type_uri=type_uri)
    # Remove the dummy values
    obj.properties[SBOL_TYPE] = []
    obj.properties[SBOL_DEFINITION] = []
    return obj


Document.register_builder(SBOL_EXTERNALLY_DEFINED, build_externally_defined)
