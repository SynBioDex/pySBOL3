from typing import Union, Any, List, Optional

import rdflib

from . import *


class BooleanPropertyMixin:

    def from_user(self, value: Any) -> Union[None, rdflib.Literal]:
        if value is None:
            return None
        if not isinstance(value, bool):
            raise TypeError(f'Expecting boolean, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value: Any) -> bool:
        return bool(value)


class BooleanSingletonProperty(BooleanPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[bool] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


class BooleanListProperty(BooleanPropertyMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[List[bool]] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


def BooleanProperty(property_owner: Any, property_uri: str,
                    lower_bound: int, upper_bound: Union[int, float],
                    validation_rules: Optional[List] = None,
                    initial_value: Optional[Union[bool, List[bool]]] = None) -> Property:
    if upper_bound == 1:
        return BooleanSingletonProperty(property_owner, property_uri,
                                        lower_bound, upper_bound,
                                        validation_rules, initial_value)
    return BooleanListProperty(property_owner, property_uri, lower_bound, upper_bound,
                               validation_rules, initial_value)
