import math
from typing import Union

from . import *


class CombinatorialDerivation(TopLevel):

    def __init__(self, name: str, template: Union[Component, str],
                 *, type_uri: str = SBOL_MODEL) -> None:
        super().__init__(name, type_uri)
        self.strategy = URIProperty(self, SBOL_STRATEGY, 0, 1)
        self.template = ReferencedObject(self, SBOL_TEMPLATE, 1, 1,
                                         initial_value=template)
        self.variable_components = OwnedObject(self, SBOL_VARIABLE_COMPONENTS,
                                               0, math.inf)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if self.strategy is not None:
            valid_strategies = [SBOL_ENUMERATE, SBOL_SAMPLE]
            if self.strategy not in valid_strategies:
                raise ValidationError(f'{self.strategy} is not a valid strategy')


def build_combinatorial_derivation(name: str,
                                   *, type_uri: str = SBOL_COMBINATORIAL_DERIVATION):
    template = PYSBOL3_MISSING
    return CombinatorialDerivation(name, template, type_uri=type_uri)


Document.register_builder(SBOL_COMBINATORIAL_DERIVATION, build_combinatorial_derivation)
