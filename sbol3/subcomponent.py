import math
from typing import Union

from . import *
# Feature is not exported
from .feature import Feature


class SubComponent(Feature):

    def __init__(self, name: str, instance_of: Union[SBOLObject, str] = None,
                 *, type_uri: str = SBOL_SUBCOMPONENT) -> None:
        super().__init__(name, type_uri)
        if instance_of is None:
            instance_of = PYSBOL3_MISSING
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
