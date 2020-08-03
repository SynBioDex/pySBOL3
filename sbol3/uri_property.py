from collections import MutableSequence
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


class URISingletonProperty(SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)

    def set(self, value: Any) -> None:
        pass

    def get(self) -> Any:
        try:
            return self.property_owner.properties[self.property_uri][0]
        except KeyError:
            return None


class URIListProperty(URIPropertyMixin, Property, MutableSequence):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)

    def __delitem__(self, key: Union[int, slice]) -> None:
        self.property_owner.properties[self.property_uri].__delitem__(key)

    def __setitem__(self, key: Union[int, slice], value: Any) -> None:
        # TODO: handle string value
        # TODO: handle list-like value
        self.property_owner.properties[self.property_uri].__setitem__(key, value)

    def __getitem__(self, key: Union[int, slice]) -> Any:
        # TODO: convert to user...
        value = self.property_owner.properties[self.property_uri].__getitem__(key)
        if isinstance(value, str):
            return self.to_user(value)
        else:
            return [self.to_user(v) for v in value]

    def __len__(self) -> int:
        return self.property_owner.properties[self.property_uri].__len__()

    def __contains__(self, item) -> bool:
        item = self.from_user(item)
        return self.property_owner.properties[self.property_uri].__contains__(item)

    def __eq__(self, other) -> bool:
        storage = self.property_owner.properties[self.property_uri]
        value = [self.to_user(v) for v in storage]
        return value.__eq__(other)

    def __str__(self) -> str:
        return self.property_owner.properties[self.property_uri].__str__()

    def __repr__(self) -> str:
        return self.property_owner.properties[self.property_uri].__repr__()

    def insert(self, index: int, value: Any) -> None:
        value = self.from_user(value)
        self.property_owner.properties[self.property_uri].insert(index, value)

    def set(self, value: Any) -> None:
        # TODO: validate here
        # TODO: test for iterable or sequence types, then convert to list?
        value = [self.from_user(v) for v in value]
        self.property_owner.properties[self.property_uri] = value


def URIProperty(property_owner: Any, property_uri: str,
                lower_bound: int, upper_bound: Union[int, float],
                validation_rules: Optional[List] = None,
                initial_value: Optional[Union[str, List[str]]] = None) -> Property:
    if upper_bound == 1:
        return URISingletonProperty(property_owner, property_uri,
                                    lower_bound, upper_bound,
                                    validation_rules, initial_value)
    return URIListProperty(property_owner, property_uri,
                           lower_bound, upper_bound,
                           validation_rules, initial_value)
