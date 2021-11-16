from __future__ import annotations
from typing import Union, Any, List, Optional

import rdflib

from . import *


class URIPropertyMixin:

    @staticmethod
    def to_user(value: Any) -> str:
        return str(value)

    @staticmethod
    def from_user(value: Any) -> rdflib.URIRef:
        if not isinstance(value, str):
            raise TypeError(f'Expecting string, got {type(value)}')
        return rdflib.URIRef(value)


class URISingletonProperty(URIPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None
                 ) -> None:
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


class URIListProperty(URIPropertyMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[Union[str, list[str]]] = None
                 ) -> None:
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            if isinstance(initial_value, str):
                # Wrap the singleton in a list
                initial_value = [initial_value]
            self.set(initial_value)


def URIProperty(property_owner: Any, property_uri: str,
                lower_bound: int, upper_bound: Union[int, float],
                *,  # require keywords from here
                validation_rules: Optional[List] = None,
                initial_value: Optional[Union[str, List[str]]] = None
                ) -> Union[str, list[str], Property]:
    if upper_bound == 1:
        return URISingletonProperty(property_owner, property_uri,
                                    lower_bound, upper_bound,
                                    validation_rules, initial_value)
    return URIListProperty(property_owner, property_uri,
                           lower_bound, upper_bound,
                           validation_rules, initial_value)
