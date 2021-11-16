from __future__ import annotations
import math
from typing import Any

from . import *
from .typing import *


class Participation(Identified):
    """Each Participation represents how a particular Feature behaves in
    its parent Interaction.

    """

    def __init__(self, roles: Union[str, list[str]],
                 participant: Union[SBOLObject, str],
                 *, name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_PARTCIPATION) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.roles: uri_list = URIProperty(self, SBOL_ROLE, 1, math.inf,
                                           initial_value=roles)
        self.participant = ReferencedObject(self, SBOL_PARTICIPANT, 1, 1,
                                            initial_value=participant)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if len(self.roles) < 1:
            message = 'Participation must have at least one role'
            report.addError(self.identity, None, message)
        if self.participant is None:
            message = 'Participation must have a participant'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_participation` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_participation method
        :return: Whatever `visitor.visit_participation` returns
        :rtype: Any

        """
        visitor.visit_participation(self)


def build_participation(identity: str,
                        *, type_uri: str = SBOL_PARTCIPATION) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Participation(roles=[missing], participant=missing,
                        identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_ROLE] = []
    obj._properties[SBOL_PARTICIPANT] = []
    return obj


Document.register_builder(SBOL_PARTCIPATION, build_participation)
