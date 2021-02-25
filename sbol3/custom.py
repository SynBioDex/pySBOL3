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
        self.rdf_type = URIProperty(self, rdflib.RDF.type, 1, 1,
                                    initial_value=sbol_type_uri)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if self.rdf_type is None:
            message = 'rdf_type is a required property of CustomIdentified'
            report.addError(self.identity, None, message)
        return report


class CustomTopLevel(TopLevel):

    def __init__(self, identity: str = None, type_uri: str = None,
                 *, attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 sbol_type_uri: str = SBOL_TOP_LEVEL) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.rdf_type = URIProperty(self, rdflib.RDF.type, 1, 1,
                                    initial_value=sbol_type_uri)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if self.rdf_type is None:
            message = 'rdf_type is a required property of CustomTopLevel'
            report.addError(self.identity, None, message)
        return report
