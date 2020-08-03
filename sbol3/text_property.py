from typing import Union, Any, List, Optional

import rdflib

from . import *


class TextSingletonProperty(SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)

    def from_user(self, value: Any) -> rdflib.Literal:
        if not isinstance(value, str):
            raise TypeError(f'Expecting string, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value: Any) -> str:
        return str(value)

    def set(self, value: Any) -> None:
        if value is None and self.lower_bound == 0:
            self.property_owner.properties[self.property_uri] = []
            return
        # TODO validate
        self.property_owner.properties[self.property_uri] = [self.from_user(value)]

    def get(self) -> Any:
        try:
            return self.to_user(self.property_owner.properties[self.property_uri][0])
        except IndexError:
            return None


def text_property(property_owner: Any, property_uri: str,
                  lower_bound: int, upper_bound: Union[int, float],
                  validation_rules: Optional[List] = None,
                  initial_value: Optional[Union[str, List[str]]] = None) -> Property:
    if upper_bound == 1:
        return TextSingletonProperty(property_owner, property_uri,
                                     lower_bound, upper_bound,
                                     validation_rules, initial_value)
    raise ValueError('Upper bound > 1 not handled yet')
