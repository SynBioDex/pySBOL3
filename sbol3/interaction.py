from __future__ import annotations
import math
from typing import List, Any

from . import *
from .typing import *


class Interaction(Identified):
    """The Interaction class provides more detailed description of how the
    Feature objects of a Component are intended to work together. For
    example, this class can be used to represent different forms of
    genetic regulation (e.g., transcriptional activation or
    repression), processes from the central dogma of biology
    (e.g. transcription and translation), and other basic molecular
    interactions (e.g., non-covalent binding or enzymatic
    phosphorylation). Each Interaction includes type properties that
    refer to descriptive ontology terms and hasParticipation
    properties that describe which Feature objects participate in
    which ways in the Interaction.

    """

    def __init__(self, types: Union[str, list[str]],
                 *, participations: List[Participation] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_INTERACTION) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.types: uri_list = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                           initial_value=types)
        self.participations = OwnedObject(self, SBOL_PARTICIPATIONS, 0, math.inf,
                                          initial_value=participations,
                                          type_constraint=Participation)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_interaction` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_interaction method
        :return: Whatever `visitor.visit_interaction` returns
        :rtype: Any

        """
        visitor.visit_interaction(self)


def build_interaction(identity: str, *, type_uri: str = SBOL_INTERACTION) -> SBOLObject:
    interaction_type = PYSBOL3_MISSING
    obj = Interaction([interaction_type], identity=identity, type_uri=type_uri)
    # Remove the placeholder type
    obj._properties[SBOL_TYPE] = []
    return obj


Document.register_builder(SBOL_INTERACTION, build_interaction)
