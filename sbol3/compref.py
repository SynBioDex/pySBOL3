from typing import Union

from . import *
# Feature is not exported
from .feature import Feature


class ComponentReference(Feature):

    def __init__(self, in_child_of: Union[SubComponent, str],
                 feature: Union[Feature, str],
                 *, identity: str = None,
                 type_uri: str = SBOL_COMPONENT_REFERENCE) -> None:
        super().__init__(identity, type_uri)
        self.in_child_of = ReferencedObject(self, SBOL_IN_CHILD_OF, 1, 1,
                                            initial_value=in_child_of)
        self.feature = ReferencedObject(self, SBOL_FEATURES, 1, 1,
                                        initial_value=feature)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # Must have 1 feature
        if self.feature is None:
            message = 'ComponentReference must have a feature'
            report.addError(self.identity, None, message)
        # Must have 1 in_child_of
        if self.in_child_of is None:
            message = 'ComponentReference must have an in_child_of reference'
            report.addError(self.identity, None, message)
        return report


def build_component_reference(identity: str, *,
                              type_uri: str = SBOL_COMPONENT_REFERENCE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = ComponentReference(missing, missing, identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_FEATURES] = []
    obj._properties[SBOL_IN_CHILD_OF] = []
    return obj


Document.register_builder(SBOL_COMPONENT_REFERENCE, build_component_reference)
