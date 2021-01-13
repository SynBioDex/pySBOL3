import math

from . import *

# Feature is not exported
from .feature import Feature
from .typing import *


class ExternallyDefined(Feature):
    """The ExternallyDefined class has been introduced so that
    external definitions in databases like ChEBI or UniProt
    can be referenced.
    """

    def __init__(self, types: List[str], definition: str,
                 *, identity: str = None,
                 type_uri: str = SBOL_EXTERNALLY_DEFINED):
        super().__init__(identity, type_uri)
        self.types: uri_list = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                           initial_value=types)
        self.definition: uri_singleton = URIProperty(self, SBOL_DEFINITION, 1, 1,
                                                     initial_value=definition)
        self.validate()

    def validate(self):
        super().validate()
        if len(self.types) < 1:
            raise ValidationError('ExternallyDefined must contain at least 1 type')
        if self.definition is None:
            raise ValidationError('ExternallyDefined must have a definition')


def build_externally_defined(identity: str,
                             *, type_uri: str = SBOL_EXTERNALLY_DEFINED) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = ExternallyDefined([missing], missing, identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_TYPE] = []
    obj._properties[SBOL_DEFINITION] = []
    return obj


Document.register_builder(SBOL_EXTERNALLY_DEFINED, build_externally_defined)
