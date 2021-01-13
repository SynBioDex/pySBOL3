import math
from typing import Union

from . import *
# Feature is not exported
from .feature import Feature


class SubComponent(Feature):

    def __init__(self, instance_of: Union[Identified, str],
                 *, identity: str = None, type_uri: str = SBOL_SUBCOMPONENT) -> None:
        super().__init__(identity, type_uri)
        self.role_integration = URIProperty(self, SBOL_ROLE, 0, 1)
        self.instance_of = ReferencedObject(self, SBOL_INSTANCE_OF, 1, 1,
                                            initial_value=instance_of)
        self.source_locations = OwnedObject(self, SBOL_SOURCE_LOCATION, 0, math.inf,
                                            type_constraint=Location)
        self.locations = OwnedObject(self, SBOL_LOCATION, 0, math.inf,
                                     type_constraint=Location)
        self.validate()

    def validate(self) -> None:
        super().validate()
        # If there is an orientation, it must be in the valid set
        if not self.instance_of:
            raise ValidationError('SubComponent must have an instance_of')


def build_subcomponent(identity: str, type_uri: str = SBOL_SUBCOMPONENT) -> Identified:
    """Used by Document to construct a SubComponent when reading an SBOL file.
    """
    missing = PYSBOL3_MISSING
    obj = SubComponent(missing, identity=identity, type_uri=type_uri)
    obj._properties[SBOL_INSTANCE_OF] = []
    return obj


Document.register_builder(SBOL_SUBCOMPONENT, build_subcomponent)
