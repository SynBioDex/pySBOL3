from typing import Optional, Union

from . import *


class Constraint(Identified):

    def __init__(self, restriction: str, subject: Union[Identified, str],
                 object: Union[Identified, str], *, identity: Optional[str] = None,
                 type_uri: str = SBOL_CONSTRAINT) -> None:
        super().__init__(identity, type_uri)
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


def build_constraint(identity: str, type_uri: str = SBOL_CONSTRAINT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Constraint(missing, missing, missing, identity=identity, type_uri=type_uri)
    obj._properties[SBOL_RESTRICTION] = []
    obj._properties[SBOL_SUBJECT] = []
    obj._properties[SBOL_OBJECT] = []
    return obj


Document.register_builder(SBOL_CONSTRAINT, build_constraint)
