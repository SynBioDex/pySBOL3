from typing import Union, Any, List, Optional, Dict

import rdflib

from . import *


class OwnedObjectPropertyMixin:

    def from_user(self, value: Any) -> rdflib.Literal:
        if not isinstance(value, str):
            raise TypeError(f'Expecting string, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value: Any) -> str:
        return str(value)

    def _storage(self) -> Dict[str, list]:
        return self.property_owner.owned_objects


class OwnedObjectSingletonProperty(OwnedObjectPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)


class OwnedObjectListProperty(OwnedObjectPropertyMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)


def OwnedObject(property_owner: Any, property_uri: str,
                lower_bound: int, upper_bound: Union[int, float],
                validation_rules: Optional[List] = None,
                initial_value: Optional[Union[str, List[str]]] = None) -> Property:
    if upper_bound == 1:
        return OwnedObjectSingletonProperty(property_owner, property_uri,
                                            lower_bound, upper_bound,
                                            validation_rules, initial_value)
    return OwnedObjectListProperty(property_owner, property_uri,
                                   lower_bound, upper_bound,
                                   validation_rules, initial_value)
