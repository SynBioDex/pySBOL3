import abc
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
        return self.property_owner.properties

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
        self._storage()[self.property_uri] = [self.from_user(value)]

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
            value = self.from_user(value)
        elif isinstance(value, Iterable):
            # string is iterable so it's broken out above
            value = [self.from_user(item) for item in value]
        else:
            # Not string or iterable
            value = self.from_user(value)
        self._storage()[self.property_uri].__setitem__(key, value)

    def __getitem__(self, key: Union[int, slice]) -> Any:
        value = self._storage()[self.property_uri].__getitem__(key)
        if isinstance(value, str):
            return self.to_user(value)
        else:
            return [self.to_user(v) for v in value]

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
        value = self.from_user(value)
        self._storage()[self.property_uri].insert(index, value)

    def set(self, value: Any) -> None:
        # TODO: validate here
        # TODO: test for iterable or sequence types, then convert to list?
        value = [self.from_user(v) for v in value]
        self._storage()[self.property_uri] = value
