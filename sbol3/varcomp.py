import math

from . import *


class VariableFeature(Identified):

    def __init__(self, *,
                 cardinality: str = None,
                 variable: str = None,
                 identity: str = None,
                 type_uri: str = SBOL_VARIABLE_FEATURE) -> None:
        super().__init__(identity, type_uri)
        # Assign default values
        if cardinality is None:
            cardinality = SBOL_ZERO_OR_MORE
        if variable is None:
            variable = PYSBOL3_MISSING
        # Create properties
        self.cardinality = URIProperty(self, SBOL_CARDINALITY, 1, 1,
                                       initial_value=cardinality)
        self.variable = ReferencedObject(self, SBOL_VARIABLE, 1, 1,
                                         initial_value=variable)
        self.variants = ReferencedObject(self, SBOL_VARIANT, 0, math.inf)
        self.variant_collections = ReferencedObject(self, SBOL_VARIANT_COLLECTION,
                                                    0, math.inf)
        self.variant_derivations = ReferencedObject(self, SBOL_VARIANT_DERIVATION,
                                                    0, math.inf)
        self.variant_measures = OwnedObject(self, SBOL_VARIANT_MEASURE,
                                            0, math.inf)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        # Cardinality must be in the set of valid URIs
        valid_cardinalities = [SBOL_ONE, SBOL_ONE_OR_MORE, SBOL_ZERO_OR_MORE,
                               SBOL_ZERO_OR_ONE]
        if self.cardinality not in valid_cardinalities:
            message = f'{self.cardinality} is not a valid cardinality'
            report.addError(None, message)
        if self.variable is None:
            message = 'VariableComponent.variable is required'
            report.addError(None, message)
        return report


Document.register_builder(SBOL_VARIABLE_FEATURE, VariableFeature)
