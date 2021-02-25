from typing import List

from . import *


class Sequence(TopLevel):

    def __init__(self, identity: str, *,
                 elements: str = None, encoding: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None, generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_SEQUENCE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.elements = TextProperty(self, SBOL_ELEMENTS, 0, 1,
                                     initial_value=elements)
        self.encoding = URIProperty(self, SBOL_ENCODING, 0, 1,
                                    initial_value=encoding)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # If sequence is set, encoding is REQUIRED
        if self.elements and not self.encoding:
            message = 'Sequence encoding is required if elements are set'
            report.addError(self.identity, None, message)
        return report


Document.register_builder(SBOL_SEQUENCE, Sequence)
