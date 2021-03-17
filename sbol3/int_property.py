from typing import Union, Any, List, Optional

import rdflib

from . import *


class IntPropertyMixin:

    def from_user(self, value: Any) -> Union[None, rdflib.Literal]:
        if value is None:
            return None
        if not isinstance(value, int):
            raise TypeError(f'Expecting int, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value: Any) -> int:
        return int(value)


class IntSingletonProperty(IntPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[int] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


class IntListProperty(IntPropertyMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[List[int]] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


def IntProperty(property_owner: Any, property_uri: str,
                lower_bound: int, upper_bound: Union[int, float],
                validation_rules: Optional[List] = None,
                initial_value: Optional[Union[int, List[int]]] = None) -> Property:
    if upper_bound == 1:
        return IntSingletonProperty(property_owner, property_uri,
                                    lower_bound, upper_bound,
                                    validation_rules, initial_value)
    return IntListProperty(property_owner, property_uri, lower_bound, upper_bound,
                           validation_rules, initial_value)
