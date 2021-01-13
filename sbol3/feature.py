import abc
import math

from . import *


class Feature(Identified, abc.ABC):
    """Feature is an abstract base class."""

    def __init__(self, identity: str, type_uri: str) -> None:
        super().__init__(identity, type_uri)
        self.roles = URIProperty(self, SBOL_ROLE, 0, math.inf)
        self.orientation = URIProperty(self, SBOL_ORIENTATION, 0, 1)

    def validate(self) -> None:
        super().validate()
        # If there is an orientation, it must be in the valid set
        if self.orientation is not None:
            valid_orientations = [SBOL_INLINE, SBOL_REVERSE_COMPLEMENT]
            if self.orientation not in valid_orientations:
                message = f'{self.orientation} is not a valid orientation'
                raise ValidationError(message)
