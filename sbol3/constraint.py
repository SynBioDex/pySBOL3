from typing import Optional, Union, List, Any

from . import *


class Constraint(Identified):
    """The Constraint class can be used to assert restrictions on the
    relationships of pairs of Feature objects contained by the same
    parent Component. Uses of this class include expressing
    containment (e.g., a plasmid transformed into a chassis strain),
    identity mappings (e.g., replacing a placeholder value with a
    complete definition), and expressing relative, sequence-based
    positions (e.g., the ordering of features within a template). Each
    Constraint includes the subject, object, and restriction
    properties.

    """

    def __init__(self, restriction: str, subject: Union[Identified, str],
                 object: Union[Identified, str], *, name: str = None,
                 description: str = None, derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: Optional[str] = None,
                 type_uri: str = SBOL_CONSTRAINT) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.restriction = URIProperty(self, SBOL_RESTRICTION, 1, 1,
                                       initial_value=restriction)
        self.subject = ReferencedObject(self, SBOL_SUBJECT, 1, 1,
                                        initial_value=subject)
        self.object = ReferencedObject(self, SBOL_OBJECT, 1, 1,
                                       initial_value=object)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if not self.restriction:
            message = 'Constraint must have a restriction'
            report.addError(self.identity, None, message)
        if not self.subject:
            message = 'Constraint must have a subject'
            report.addError(self.identity, None, message)
        if not self.object:
            message = 'Constraint must have an object'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_constraint` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_constraint method
        :return: Whatever `visitor.visit_constraint` returns
        :rtype: Any

        """
        visitor.visit_constraint(self)


def build_constraint(identity: str, type_uri: str = SBOL_CONSTRAINT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Constraint(missing, missing, missing, identity=identity, type_uri=type_uri)
    obj._properties[SBOL_RESTRICTION] = []
    obj._properties[SBOL_SUBJECT] = []
    obj._properties[SBOL_OBJECT] = []
    return obj


Document.register_builder(SBOL_CONSTRAINT, build_constraint)
