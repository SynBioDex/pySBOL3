import math
from typing import List, Union

from . import *


class Component(TopLevel):

    def __init__(self) -> None:
        super().__init__()
        self.roles = URIProperty(self, SBOL_ROLE, 0, math.inf)
        self.types: Union[List, Property] = URIProperty(self, SBOL_TYPE, 1, math.inf)
        self.sequences = URIProperty(self, SBOL_SEQUENCES, 0, math.inf)
        self.models = URIProperty(self, SBOL_MODELS, 0, math.inf)

    def _validate_types(self) -> None:
        # A Component is REQUIRED to have one or more type properties (Section 6.4)
        if len(self.types) < 1:
            message = f'Component {self.identity} has no types'
            raise ValidationError(message)

    def validate(self) -> None:
        super().validate()
        self._validate_types()
