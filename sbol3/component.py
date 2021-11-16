from __future__ import annotations

import math
from typing import Any, Optional
import typing

from . import *
from .typing import *


class Component(TopLevel):

    def __init__(self, identity: str, types: Optional[Union[str, typing.Sequence[str]]],
                 *,  # Keywords only after this
                 roles: Optional[Union[str, typing.Sequence[str]]] = None,
                 sequences: Optional[refobj_list_arg] = None,
                 features: Union[Feature, typing.Sequence[Feature]] = None,
                 constraints: Union[Constraint, typing.Sequence[Constraint]] = None,
                 interactions: Union[Interaction, typing.Sequence[Interaction]] = None,
                 interface: Union[Interface, typing.Sequence[Interface]] = None,
                 models: Optional[refobj_list_arg] = None,
                 namespace: Optional[str] = None,
                 attachments: Optional[refobj_list_arg] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 derived_from: Optional[Union[str, typing.Sequence[str]]] = None,
                 generated_by: Optional[refobj_list_arg] = None,
                 measures: Optional[ownedobj_list_arg] = None,
                 type_uri: str = SBOL_COMPONENT) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.types = URIProperty(self, SBOL_TYPE, 1, math.inf,
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
        self.interface = OwnedObject(self, SBOL_INTERFACES, 0, 1,
                                     initial_value=interface,
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
