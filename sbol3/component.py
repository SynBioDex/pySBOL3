import math
from typing import List, Union, Any

from . import *


class Component(TopLevel):

    def __init__(self, identity: str, types: Union[List[str], str],
                 *, roles: List[str] = None,
                 sequences: List[str] = None,
                 features: List[Feature] = None,
                 constraints: List[Constraint] = None,
                 interactions: List[Interaction] = None,
                 interfaces: List[Interface] = None,
                 models: List[str] = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None, generated_by: List[str] = None,
                 measures: List[SBOLObject] = None, type_uri: str = SBOL_COMPONENT):
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        if isinstance(types, str):
            types = [types]
        self.types: Union[List, Property] = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                                        initial_value=types)
        self.roles = URIProperty(self, SBOL_ROLE, 0, math.inf,
                                 initial_value=roles)
        self.sequences = ReferencedObject(self, SBOL_SEQUENCES, 0, math.inf,
                                          initial_value=sequences)
        self.features = OwnedObject(self, SBOL_FEATURES, 0, math.inf,
                                    initial_value=features,
                                    type_constraint=Feature)
        self.interactions = OwnedObject(self, SBOL_INTERACTIONS, 0, math.inf,
                                        initial_value=interactions,
                                        type_constraint=Interaction)
        self.constraints = OwnedObject(self, SBOL_CONSTRAINTS, 0, math.inf,
                                       initial_value=constraints,
                                       type_constraint=Constraint)
        self.interfaces = OwnedObject(self, SBOL_INTERFACES, 0, 1,
                                      initial_value=interfaces,
                                      type_constraint=Interface)
        self.models = ReferencedObject(self, SBOL_MODELS, 0, math.inf,
                                       initial_value=models)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_component` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_component method
        :return: Whatever `visitor.visit_component` returns
        :rtype: Any

        """
        visitor.visit_component(self)


def build_component(identity: str, *, type_uri: str = SBOL_COMPONENT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Component(identity, [missing], type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_TYPE] = []
    return obj


Document.register_builder(SBOL_COMPONENT, build_component)
