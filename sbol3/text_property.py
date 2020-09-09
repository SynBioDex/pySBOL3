from typing import Union, Any, List, Optional

import rdflib

from . import *


class TextPropertyMixin:

    def from_user(self, value: Any) -> Union[None, rdflib.Literal]:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(f'Expecting string, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value: Any) -> str:
        return str(value)


class TextSingletonProperty(TextPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)


class TextListProperty(TextPropertyMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)


def TextProperty(property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: Union[int, float],
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[Union[str, List[str]]] = None) -> Property:
    if upper_bound == 1:
        return TextSingletonProperty(property_owner, property_uri,
                                     lower_bound, upper_bound,
                                     validation_rules, initial_value)
    return TextListProperty(property_owner, property_uri,
                            lower_bound, upper_bound,
                            validation_rules, initial_value)
