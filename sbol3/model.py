from typing import List

from . import *


class Model(TopLevel):
    """The purpose of the Model class is to serve as a placeholder for an
    external computational model and provide additional meta-data to
    enable better reasoning about the contents of this model. In this
    way, there is minimal duplication of standardization efforts and
    users of SBOL can elaborate descriptions of Component function in
    the language of their choice.

    """

    def __init__(self, identity: str, source: str, language: str,
                 framework: str,
                 *, attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_MODEL) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.source = URIProperty(self, SBOL_SOURCE, 1, 1,
                                  initial_value=source)
        self.language = URIProperty(self, SBOL_LANGUAGE, 1, 1,
                                    initial_value=language)
        self.framework = URIProperty(self, SBOL_FRAMEWORK, 1, 1,
                                     initial_value=framework)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # The source property is REQUIRED and MUST contain a URI reference (Section 6.8)
        if not self.source:
            msg = f'Model {self.identity} does not have a source'
            report.addError(self.identity, None, msg)
        # The language property is REQUIRED and MUST contain a URI (Section 6.8)
        if not self.language:
            msg = f'Model {self.identity} does not have a language'
            report.addError(self.identity, None, msg)
        # The framework property is REQUIRED and MUST contain a URI (Section 6.8)
        if not self.framework:
            msg = f'Model {self.identity} does not have a framework'
            report.addError(self.identity, None, msg)
        return report


def build_model(identity: str, type_uri: str = SBOL_MODEL):
    """Used by Document to construct a Range when reading an SBOL file.
    """
    obj = Model(identity=identity, source=PYSBOL3_MISSING,
                language=PYSBOL3_MISSING, framework=PYSBOL3_MISSING,
                type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_SOURCE] = []
    obj._properties[SBOL_LANGUAGE] = []
    obj._properties[SBOL_FRAMEWORK] = []
    return obj


Document.register_builder(SBOL_MODEL, build_model)
