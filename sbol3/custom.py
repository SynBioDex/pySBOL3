from typing import List

import rdflib

from . import *


class CustomIdentified(Identified):

    def __init__(self, type_uri: str = None,
                 *, name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 sbol_type_uri: str = SBOL_IDENTIFIED) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self._rdf_types.append(sbol_type_uri)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if len(self._rdf_types) < 2:
            message = 'Extension classes must have at least 2 rdf:type properties'
            report.addError(self.identity, None, message)
        return report


class CustomTopLevel(TopLevel):

    def __init__(self, identity: str = None, type_uri: str = None,
                 *, namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 sbol_type_uri: str = SBOL_TOP_LEVEL) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self._rdf_types.append(sbol_type_uri)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if len(self._rdf_types) < 2:
            message = 'Extension classes must have at least 2 rdf:type properties'
            report.addError(self.identity, None, message)
        return report
