from typing import Union, Any, List, Optional

import rdflib

from . import *


class ReferencedURI(str):

    def __eq__(self, other):
        return super().__eq__(other)

    def lookup(self):
        if hasattr(self, 'parent'):
            print(f'Property owner = {self.parent}')
            return self.parent.document.find(str(self))
        else:
            # TODO: Should the lack of a parent raise an error?
            return None


class ReferencedObjectMixin:

    def to_user(self, value: Any) -> str:
        result = ReferencedURI(str(value))
        if hasattr(self, 'property_owner'):
            parent = self.property_owner
            result.parent = parent
        return result

    @staticmethod
    def from_user(value: Any) -> rdflib.URIRef:
        if not isinstance(value, str):
            raise TypeError(f'Expecting string, got {type(value)}')
        return rdflib.URIRef(value)


class ReferencedObjectSingleton(ReferencedObjectMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)


class ReferencedObjectList(ReferencedObjectMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value:
            self.set(initial_value)


def ReferencedObject(property_owner: Any, property_uri: str,
                     lower_bound: int, upper_bound: Union[int, float],
                     validation_rules: Optional[List] = None,
                     initial_value: Optional[Union[str, List[str]]] = None) -> Property:
    if upper_bound == 1:
        return ReferencedObjectSingleton(property_owner, property_uri,
                                         lower_bound, upper_bound,
                                         validation_rules, initial_value)
    return ReferencedObjectList(property_owner, property_uri,
                                lower_bound, upper_bound,
                                validation_rules, initial_value)
