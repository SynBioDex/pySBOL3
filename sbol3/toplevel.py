import math
from typing import List

from . import *


class TopLevel(Identified):

    def __init__(self, identity: str, type_uri: str,
                 *, attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None) -> None:
        # Sanity check identity, which is required for a TopLevel
        # More checking on identity happens in Identified, but Identified
        # does not require an identity, only TopLevel does.
        if not identity or not isinstance(identity, str):
            raise ValueError('Identity must be a non-empty string')
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.attachments = ReferencedObject(self, SBOL_HAS_ATTACHMENT, 0, math.inf,
                                            initial_value=attachments)

    def validate_identity(self, report: ValidationReport) -> None:
        # TODO: See section 5.1 for rules about identity for TopLevel
        pass

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        return report
