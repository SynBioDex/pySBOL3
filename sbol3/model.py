from . import *


class Model(TopLevel):

    def __init__(self, identity: str, *, type_uri: str = SBOL_MODEL) -> None:
        super().__init__(identity, type_uri)
        self.source = URIProperty(self, SBOL_SOURCE, 1, 1)
        self.language = URIProperty(self, SBOL_LANGUAGE, 1, 1)
        self.framework = URIProperty(self, SBOL_FRAMEWORK, 1, 1)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # The source property is REQUIRED and MUST contain a URI reference (Section 6.8)
        if not self.source:
            msg = f'Model {self.identity} does not have a source'
            report.addError(None, msg)
        # The language property is REQUIRED and MUST contain a URI (Section 6.8)
        if not self.language:
            msg = f'Model {self.identity} does not have a language'
            report.addError(None, msg)
        # The framework property is REQUIRED and MUST contain a URI (Section 6.8)
        if not self.framework:
            msg = f'Model {self.identity} does not have a framework'
            report.addError(None, msg)
        return report


Document.register_builder(SBOL_MODEL, Model)
