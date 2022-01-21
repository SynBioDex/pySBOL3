import posixpath
from typing import Union, Any, List, Optional, Dict

import rdflib

from . import *
from .utils import parse_class_name


class OwnedObjectPropertyMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_constraint = None

    def from_user(self, value: Any) -> rdflib.Literal:
        desired_type = SBOLObject
        if self.type_constraint:
            desired_type = self.type_constraint
        if not isinstance(value, desired_type):
            raise TypeError(f'Expecting {desired_type}, got {type(value)}')
        return value

    def to_user(self, value: Any) -> str:
        return value

    def _storage(self) -> Dict[str, list]:
        return self.property_owner._owned_objects

    def item_added(self, item: Any) -> None:
        # First, set the document
        if hasattr(item, 'document'):
            item.document = self.property_owner.document
        if not self.property_owner.identity_is_url():
            return
        # if not item.display_id:
        #     raise ValueError(f'Item {item} does not have a display_id')
        type_name = parse_class_name(item.type_uri)
        counter_value = self.property_owner.counter_value(type_name)
        # Provide stability across clone and copy
        # If an item already has a display_id, use it, otherwise mint a new one
        if item.display_id:
            new_display_id = item.display_id
        else:
            new_display_id = f'{type_name}{counter_value}'
        new_url = posixpath.join(self.property_owner.identity, new_display_id)
        for sibling in self._storage()[self.property_uri]:
            if sibling == item:
                continue
            if sibling.identity == new_url:
                raise ValueError(f'Duplicate URI: {new_url}')
        item._update_identity(new_url, new_display_id)

    def validate_type_constraint(self, name: str, report: ValidationReport):
        if not self.type_constraint:
            return
        for item in self._storage()[self.property_uri]:
            if not isinstance(item, self.type_constraint):
                msg = f'Value {item} is not of type {self.type_constraint}'
                report.addError(self.property_owner.identity, None, msg)


class OwnedObjectSingletonProperty(OwnedObjectPropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None,
                 type_constraint: Optional[Any] = None):
        super().__init__(property_owner=property_owner,
                         property_uri=property_uri,
                         lower_bound=lower_bound,
                         upper_bound=upper_bound,
                         validation_rules=validation_rules)
        # Better to pass this up to super, but the super().__init__
        # methods are not set up properly for that. They would need
        # to accept unknown keyword arguments.
        self.type_constraint = type_constraint
        if initial_value is not None:
            self.set(initial_value)

    def validate(self, name: str, report: ValidationReport):
        # Invoke Property.validate()
        super().validate(name, report)
        # Invoke OwnedObjectPropertyMixin type constraint checking
        super().validate_type_constraint(name, report)


class OwnedObjectListProperty(OwnedObjectPropertyMixin, ListProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None,
                 type_constraint: Optional[Any] = None):
        super().__init__(property_owner=property_owner,
                         property_uri=property_uri,
                         lower_bound=lower_bound,
                         upper_bound=upper_bound,
                         validation_rules=validation_rules)
        # Better to pass this up to super, but the super().__init__
        # methods are not set up properly for that. They would need
        # to accept unknown keyword arguments.
        self.type_constraint = type_constraint
        if initial_value is not None:
            if isinstance(initial_value, SBOLObject):
                # coerce the singleton into a list
                # see https://github.com/SynBioDex/pySBOL3/issues/301
                initial_value = [initial_value]
            self.set(initial_value)

    def validate(self, name: str, report: ValidationReport):
        # Invoke Property.validate()
        super().validate(name, report)
        # Invoke OwnedObjectPropertyMixin type constraint checking
        super().validate_type_constraint(name, report)


def OwnedObject(property_owner: Any, property_uri: str,
                lower_bound: int, upper_bound: Union[int, float],
                validation_rules: Optional[List] = None,
                initial_value: Optional[Union['Identified', List['Identified']]] = None,
                type_constraint: Optional[Any] = None
                ) -> Property:
    if upper_bound == 1:
        return OwnedObjectSingletonProperty(property_owner, property_uri,
                                            lower_bound, upper_bound,
                                            validation_rules, initial_value,
                                            type_constraint=type_constraint)
    return OwnedObjectListProperty(property_owner, property_uri,
                                   lower_bound, upper_bound,
                                   validation_rules, initial_value,
                                   type_constraint=type_constraint)
