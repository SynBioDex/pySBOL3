import abc
import collections
from collections import MutableSequence, Iterable
from typing import Any, Optional, List, Dict, Union


class Property(abc.ABC):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None) -> None:
        self.property_owner = property_owner
        self.property_uri = property_uri
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        if validation_rules is None:
            validation_rules = []
        self.validation_rules = validation_rules
        # Initialize the storage for this property
        self._storage()[self.property_uri] = []

    def _storage(self) -> Dict[str, list]:
        return self.property_owner._properties

    @abc.abstractmethod
    def set(self, value: Any) -> None:
        pass

    @abc.abstractmethod
    def to_user(self, value: Any) -> str:
        pass

    @abc.abstractmethod
    def from_user(self, value: Any):
        pass


class SingletonProperty(Property, abc.ABC):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None) -> None:
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound,
                         validation_rules)
        # This is a marker for SBOLObject.__get_attribute__
        self._sbol_singleton = True

    def set(self, value: Any) -> None:
        value = self.from_user(value)
        if value is None:
            if self.lower_bound == 0:
                self._storage()[self.property_uri] = []
            else:
                raise ValueError(f'Property {self.property_uri} cannot be unset')
        else:
            self._storage()[self.property_uri] = [value]

    def get(self) -> Any:
        try:
            value = self._storage()[self.property_uri][0]
        except IndexError:
            return None
        return self.to_user(value)


class ListProperty(Property, MutableSequence, abc.ABC):

    def __delitem__(self, key: Union[int, slice]) -> None:
        self._storage()[self.property_uri].__delitem__(key)

    def __setitem__(self, key: Union[int, slice], value: Any) -> None:
        # Do string separately because it, too, is iterable
        if isinstance(value, str):
            values = [value]
            value = self.from_user(value)
        elif isinstance(value, Iterable):
            # string is iterable so it's broken out above
            values = value
            value = [self.from_user(item) for item in value]
        else:
            # Not string or iterable
            values = [value]
            value = self.from_user(value)
        self._storage()[self.property_uri].__setitem__(key, value)
        for val in values:
            self.item_added(val)

    def __getitem__(self, key: Union[int, slice]) -> Any:
        value = self._storage()[self.property_uri].__getitem__(key)
        if isinstance(value, str):
            return self.to_user(value)
        elif isinstance(value, collections.Iterable):
            return [self.to_user(v) for v in value]
        else:
            # Not a string or an iterable, just convert
            return self.to_user(value)

    def __len__(self) -> int:
        return self._storage()[self.property_uri].__len__()

    def __contains__(self, item) -> bool:
        item = self.from_user(item)
        return self._storage()[self.property_uri].__contains__(item)

    def __eq__(self, other) -> bool:
        storage = self._storage()[self.property_uri]
        value = [self.to_user(v) for v in storage]
        return value.__eq__(other)

    def __str__(self) -> str:
        return str([self.to_user(item)
                    for item in self._storage()[self.property_uri]])

    def __repr__(self) -> str:
        return repr([self.to_user(item)
                     for item in self._storage()[self.property_uri]])

    def insert(self, index: int, value: Any) -> None:
        item = self.from_user(value)
        self._storage()[self.property_uri].insert(index, item)
        self.item_added(value)

    def set(self, value: Any) -> None:
        # TODO: validate here
        # TODO: test for iterable or sequence types, then convert to list?
        items = [self.from_user(v) for v in value]
        self._storage()[self.property_uri] = items
        for val in value:
            self.item_added(val)

    def item_added(self, item: Any) -> None:
        """Stub method for child classes to override if they have to do
        any additional processing on items after they are added. This method
        will be called on each individual item that was added to the list.
        """
        pass
