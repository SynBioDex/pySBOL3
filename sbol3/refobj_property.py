from __future__ import annotations

from typing import Union, Any, List, Optional

import rdflib

from . import *


class ReferencedURI(str):

    def __eq__(self, other):
        return super().__eq__(other)

    def lookup(self):
        if hasattr(self, 'parent'):
            return self.parent.document.find(str(self))
        else:
            # TODO: Should the lack of a parent raise an error?
            return None


class ReferencedObjectMixin:

    def to_user(self, value: Any) -> str:
        if hasattr(self, 'property_owner'):
            parent = self.property_owner
            value.parent = parent
        # Should we check to see if value has a document as well?
        return value

    #@staticmethod
    def from_user(self, value: Any) -> rdflib.URIRef:
        #if isinstance(value, SBOLObject):
        #    # see https://github.com/SynBioDex/pySBOL3/issues/357
        #    if value.identity is None:
        #        # The SBOLObject has an uninitialized identity
        #        msg = f'Cannot set reference to {value}.'
        #        msg += ' Object identity is uninitialized.'
        #        raise ValueError(msg)
        #    value = value.identity
        #if not isinstance(value, str):
        #    raise TypeError(f'Expecting string, got {type(value)}')

        # TODO: what is value is empty string?
        if type(value) is str:
            if self.property_owner.document:
                value = self.property_owner.document.find(value)
                # TODO: warn user referenced object is not in document
                if value is not None:
                    return value
            # If not found in Document
            value = SBOLObject(value)
        if not isinstance(value, SBOLObject):
            raise TypeError('Cannot set property, the value must be str or instance of SBOLObect')
        return value

    def maybe_add_to_document(self, value: Any) -> None:
        # if not isinstance(value, TopLevel):
        #     return
        if hasattr(self, 'property_owner'):
            if self.property_owner and self.property_owner.document:
                try:
                    self.property_owner.document.add(value)
                except TypeError:
                    # Not an appropriate type to be added, ignore
                    pass


class ReferencedObjectSingleton(ReferencedObjectMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[Union[Identified, str]] = None) -> None:
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)

    def set(self, value: Any) -> None:
        super().set(value)
        # See bug 184 - don't add to document
        # self.maybe_add_to_document(value)


class ReferencedObjectList(ReferencedObjectMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[list[Union[Identified, str]]] = None) -> None:
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            # Cannot use 'Identified' here because it isn't defined yet
            if isinstance(initial_value, (str, SBOLObject)):
                # Wrap the singleton in a list
                initial_value = [initial_value]
            self.set(initial_value)

    # See bug 184 - don't add to document
    # def item_added(self, item: Any) -> None:
    #     self.maybe_add_to_document(item)


def ReferencedObject(property_owner: Any, property_uri: str,
                     lower_bound: int, upper_bound: Union[int, float],
                     validation_rules: Optional[List] = None,
                     initial_value: Optional[Union[Union[Identified, str],
                                                   list[Union[Identified, str]]]] = None
                     ) -> Union[ReferencedURI, list[ReferencedURI], Property]:
    if upper_bound == 1:
        return ReferencedObjectSingleton(property_owner, property_uri,
                                         lower_bound, upper_bound,
                                         validation_rules, initial_value)
    return ReferencedObjectList(property_owner, property_uri,
                                lower_bound, upper_bound,
                                validation_rules, initial_value)
