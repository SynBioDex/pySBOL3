import math
from typing import Union, List, Any, Optional

from . import *


class CombinatorialDerivation(TopLevel):
    """The purpose of the CombinatorialDerivation class is to specify
    combinatorial biological designs without having to specify every
    possible design variant. For example, a CombinatorialDerivation
    can be used to specify a library of reporter gene variants that
    include different promoters and RBSs without having to specify a
    Component for every possible combination of promoter, RBS, and CDS
    in the library. Component objects that realize a
    CombinatorialDerivation can be derived in accordance with the
    class properties template, hasVariableFeature, and strategy.

    """

    def __init__(self, identity: str, template: Union[Component, str],
                 *, strategy: Optional[str] = None,
                 variable_features: List[str] = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_COMBINATORIAL_DERIVATION) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.strategy = URIProperty(self, SBOL_STRATEGY, 0, 1,
                                    initial_value=strategy)
        self.template = ReferencedObject(self, SBOL_TEMPLATE, 1, 1,
                                         initial_value=template)
        self.variable_features = OwnedObject(self, SBOL_VARIABLE_FEATURES,
                                             0, math.inf,
                                             initial_value=variable_features,
                                             type_constraint=VariableFeature)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if self.strategy is not None:
            valid_strategies = [SBOL_ENUMERATE, SBOL_SAMPLE]
            if self.strategy not in valid_strategies:
                message = f'{self.strategy} is not a valid strategy'
                report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_combinatorial_derivation` on `visitor` with `self`
        as the only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_combinatorial_derivation
                                method
        :return: Whatever `visitor.visit_combinatorial_derivation` returns
        :rtype: Any

        """
        visitor.visit_combinatorial_derivation(self)


def build_combinatorial_derivation(identity: str,
                                   *, type_uri: str = SBOL_COMBINATORIAL_DERIVATION):
    template = PYSBOL3_MISSING
    return CombinatorialDerivation(identity, template, type_uri=type_uri)


Document.register_builder(SBOL_COMBINATORIAL_DERIVATION, build_combinatorial_derivation)
