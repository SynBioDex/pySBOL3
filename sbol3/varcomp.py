import math
from typing import List, Union, Any

from . import *
from .typing import uri_singleton


class VariableFeature(Identified):
    """As described above, the VariableComponent VariableFeature class
    specifies a variable and set of values that will replace one of
    the SubComponent Feature objects in the template of a
    CombinatorialDerivation. The variable is specified by the variable
    property, and the set of values is defined by the union of
    Component objects referred to by the variant, variantCollection,
    and variantDerivation properties.

    """

    def __init__(self, cardinality: str, variable: Union[Identified, str],
                 *, variants: List[Union[Identified, str]] = None,
                 # We really need to define our own types...
                 variant_collections: Union[Union[Identified, str],
                                            List[Union[Identified, str]]] = None,
                 variant_derivations: List[Union[Identified, str]] = None,
                 variant_measures: List[Union[Identified, str]] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_VARIABLE_FEATURE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        # Assign default values
        if cardinality is None:
            cardinality = SBOL_ZERO_OR_MORE
        if variable is None:
            variable = PYSBOL3_MISSING
        # Create properties
        self.cardinality: uri_singleton = URIProperty(self, SBOL_CARDINALITY, 1, 1,
                                                      initial_value=cardinality)
        self.variable = ReferencedObject(self, SBOL_VARIABLE, 1, 1,
                                         initial_value=variable)
        self.variants = ReferencedObject(self, SBOL_VARIANT, 0, math.inf,
                                         initial_value=variants)
        self.variant_collections = ReferencedObject(self, SBOL_VARIANT_COLLECTION,
                                                    0, math.inf,
                                                    initial_value=variant_collections)
        self.variant_derivations = ReferencedObject(self, SBOL_VARIANT_DERIVATION,
                                                    0, math.inf,
                                                    initial_value=variant_derivations)
        self.variant_measures = OwnedObject(self, SBOL_VARIANT_MEASURE,
                                            0, math.inf,
                                            initial_value=variant_measures)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # Cardinality must be in the set of valid URIs
        valid_cardinalities = [SBOL_ONE, SBOL_ONE_OR_MORE, SBOL_ZERO_OR_MORE,
                               SBOL_ZERO_OR_ONE]
        if self.cardinality not in valid_cardinalities:
            message = f'{self.cardinality} is not a valid cardinality'
            report.addError(self.identity, None, message)
        if self.variable is None:
            message = 'VariableComponent.variable is required'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_variable_feature` on `visitor` with `self` as the
        only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_variable_feature method
        :return: Whatever `visitor.visit_variable_feature` returns
        :rtype: Any

        """
        visitor.visit_variable_feature(self)


def build_variable_feature(identity: str, type_uri: str = SBOL_VARIABLE_FEATURE):
    """Used by Document to construct a VariableFeature when reading an SBOL file.
    """
    obj = VariableFeature(cardinality=PYSBOL3_MISSING, variable=PYSBOL3_MISSING,
                          identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_CARDINALITY] = []
    obj._properties[SBOL_VARIABLE] = []
    return obj


Document.register_builder(SBOL_VARIABLE_FEATURE, build_variable_feature)
