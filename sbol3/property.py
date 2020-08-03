import abc
from typing import Any, Optional, List, Dict


class Property(abc.ABC):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None) -> None:
        if not hasattr(property_owner, 'properties'):
            raise TypeError('Property owner has no "properties" attribute')
        self.property_owner = property_owner
        self.property_uri = property_uri
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        if validation_rules is None:
            validation_rules = []
        self.validation_rules = validation_rules
        # Initialize the storage for this property
        self._storage[self.property_uri] = []

    @abc.abstractmethod
    def set(self, value: Any) -> None:
        pass

    @property
    def _storage(self) -> Dict[str, list]:
        return self.property_owner.properties


class SingletonProperty(Property, abc.ABC):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None) -> None:
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound,
                         validation_rules)
        # This is a marker for SBOLObject.__get_attribute__
        self._sbol_singleton = True

    @abc.abstractmethod
    def get(self) -> Any:
        pass
