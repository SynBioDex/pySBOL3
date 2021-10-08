from typing import Union, List, Any

from . import *
# Feature is not exported
from .feature import Feature


class ComponentReference(Feature):
    """ComponentReference can be used to reference Features within
    SubComponents.

    """

    def __init__(self, in_child_of: Union[SubComponent, str],
                 refers_to: Union[Feature, str],
                 *, roles: List[str] = None, orientation: str = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_COMPONENT_REFERENCE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         roles=roles, orientation=orientation, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.in_child_of = ReferencedObject(self, SBOL_IN_CHILD_OF, 1, 1,
                                            initial_value=in_child_of)
        self.refers_to = ReferencedObject(self, SBOL_REFERS_TO, 1, 1,
                                          initial_value=refers_to)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # Must have 1 refersTo
        if self.refers_to is None:
            message = 'ComponentReference must have a feature'
            report.addError(self.identity, None, message)
        # Must have 1 in_child_of
        if self.in_child_of is None:
            message = 'ComponentReference must have an in_child_of reference'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_component_reference` on `visitor` with `self` as the
        only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_component_reference
                                method
        :return: Whatever `visitor.visit_component_reference` returns
        :rtype: Any

        """
        visitor.visit_component_reference(self)


def build_component_reference(identity: str, *,
                              type_uri: str = SBOL_COMPONENT_REFERENCE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = ComponentReference(missing, missing, identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_FEATURES] = []
    obj._properties[SBOL_IN_CHILD_OF] = []
    return obj


Document.register_builder(SBOL_COMPONENT_REFERENCE, build_component_reference)
