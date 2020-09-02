from typing import Union, Any, List, Optional

import rdflib

from . import *


class FloatPropertyMixin:

    def from_user(self, value: Union[float, int, None]) -> Union[None, rdflib.Literal]:
        if value is None:
            return None
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError(f'Expecting float, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value: Any) -> float:
        return float(value)


class FloatSingletonProperty(FloatPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Union[float, int, None] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


def FloatProperty(property_owner: Any, property_uri: str,
                  lower_bound: int, upper_bound: Union[int, float],
                  validation_rules: Optional[List] = None,
                  initial_value: Optional[Union[float, List[float]]] = None) -> Property:
    if upper_bound == 1:
        return FloatSingletonProperty(property_owner, property_uri,
                                      lower_bound, upper_bound,
                                      validation_rules, initial_value)
    raise ValueError('Upper bound > 1 not handled yet')
