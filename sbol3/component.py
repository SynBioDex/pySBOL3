import math
from typing import List, Union

from . import *


class Component(TopLevel):

    def __init__(self, identity: str, component_type: Union[List[str], str],
                 *, type_uri: str = SBOL_COMPONENT):
        super().__init__(identity, type_uri)
        if isinstance(component_type, str):
            component_type = [component_type]
        self.types: Union[List, Property] = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                                        initial_value=component_type)
        self.roles = URIProperty(self, SBOL_ROLE, 0, math.inf)
        self.sequences = ReferencedObject(self, SBOL_SEQUENCES, 0, math.inf)
        self.features = OwnedObject(self, SBOL_FEATURES, 0, math.inf,
                                    type_constraint=Feature)
        self.interactions = OwnedObject(self, SBOL_INTERACTIONS, 0, math.inf,
                                        type_constraint=Interaction)
        self.constraints = OwnedObject(self, SBOL_CONSTRAINTS, 0, math.inf,
                                       type_constraint=Constraint)
        self.interfaces = OwnedObject(self, SBOL_INTERFACES, 0, 1,
                                      type_constraint=Interface)
        self.models = ReferencedObject(self, SBOL_MODELS, 0, math.inf)
        self.validate()

    def _validate_types(self) -> None:
        # A Component is REQUIRED to have one or more type properties (Section 6.4)
        if len(self.types) < 1:
            message = f'Component {self.identity} has no types'
            raise ValidationError(message)

    def validate(self) -> None:
        super().validate()
        self._validate_types()


def build_component(identity: str, *, type_uri: str = SBOL_COMPONENT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Component(identity, [missing], type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_TYPE] = []
    return obj


Document.register_builder(SBOL_COMPONENT, build_component)
