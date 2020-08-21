import math
from typing import Union

from . import *
# Feature is not exported
from .feature import Feature


class SubComponent(Feature):

    @staticmethod
    def _builder(identity_uri: str, type_uri: str = SBOL_SUBCOMPONENT):
        """Used by Document to construct a SubComponent when reading an SBOL file.
        """
        return SubComponent(identity_uri, PYSBOL3_MISSING, type_uri=type_uri)

    def __init__(self, name: str, instance_of: Union[SBOLObject, str],
                 *, type_uri: str = SBOL_SUBCOMPONENT) -> None:
        super().__init__(name, type_uri)
        self.role_integration = URIProperty(self, SBOL_ROLE, 0, 1)
        self.instance_of = ReferencedObject(self, SBOL_INSTANCE_OF, 1, 1,
                                            initial_value=instance_of)
        self.source_locations = OwnedObject(self, SBOL_SOURCE_LOCATION, 0, math.inf)
        self.locations = OwnedObject(self, SBOL_LOCATION, 0, math.inf)

    def validate(self) -> None:
        super().validate()
        # If there is an orientation, it must be in the valid set
        if self.orientation is not None:
            valid_orientations = [SBOL_INLINE, SBOL_REVERSE_COMPLEMENT]
            if self.orientation not in valid_orientations:
                message = f'{self.orientation} is not a valid orientation'
                raise ValidationError(message)


Document.register_builder(SBOL_SUBCOMPONENT, SubComponent._builder)
