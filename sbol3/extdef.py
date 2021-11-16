from __future__ import annotations
import math
from typing import Any

from . import *

# Feature is not exported
from .feature import Feature
from .typing import *


class ExternallyDefined(Feature):
    """The ExternallyDefined class has been introduced so that
    external definitions in databases like ChEBI or UniProt
    can be referenced.

    """

    def __init__(self, types: Union[str, list[str]], definition: str,
                 *, roles: List[str] = None, orientation: str = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_EXTERNALLY_DEFINED):
        super().__init__(identity=identity, type_uri=type_uri,
                         roles=roles, orientation=orientation, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.types: uri_list = URIProperty(self, SBOL_TYPE, 1, math.inf,
                                           initial_value=types)
        self.definition: uri_singleton = URIProperty(self, SBOL_DEFINITION, 1, 1,
                                                     initial_value=definition)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if len(self.types) < 1:
            message = 'ExternallyDefined must contain at least 1 type'
            report.addError(self.identity, None, message)
        if self.definition is None:
            message = 'ExternallyDefined must have a definition'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_externally_defined` on `visitor` with `self` as the
        only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_externally_defined
                                method
        :return: Whatever `visitor.visit_externally_defined` returns
        :rtype: Any

        """
        visitor.visit_externally_defined(self)


def build_externally_defined(identity: str,
                             *, type_uri: str = SBOL_EXTERNALLY_DEFINED) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = ExternallyDefined([missing], missing, identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_TYPE] = []
    obj._properties[SBOL_DEFINITION] = []
    return obj


Document.register_builder(SBOL_EXTERNALLY_DEFINED, build_externally_defined)
