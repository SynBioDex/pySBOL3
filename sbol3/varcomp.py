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
        self.variant = ReferencedObject(self, SBOL_VARIANT, 0, math.inf)
        self.variant_collection = ReferencedObject(self, SBOL_VARIANT_COLLECTION,
                                                   0, math.inf)
        self.variant_derivation = ReferencedObject(self, SBOL_VARIANT_DERIVATION,
                                                   0, math.inf)
        self.variant_measure = OwnedObject(self, SBOL_VARIANT_MEASURE,
                                           0, math.inf)
        # Validate
        self.validate()

    def validate(self) -> None:
        super().validate()
        # Cardinality must be in the set of valid URIs
        valid_cardinalities = [SBOL_ONE, SBOL_ONE_OR_MORE, SBOL_ZERO_OR_MORE,
                               SBOL_ZERO_OR_ONE]
        if self.cardinality not in valid_cardinalities:
            raise ValidationError(f'{self.cardinality} is not a valid cardinality')
        if self.variable is None:
            raise ValidationError('VariableComponent.variable is required')
