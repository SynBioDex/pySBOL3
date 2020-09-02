import datetime
from typing import Union, Any, List, Optional

import dateutil.parser
import rdflib

from . import *


class DateTimePropertyMixin:

    def from_user(self, value):
        # None is ok iff upper bound is 1 and lower bound is 0.
        # If upper bound > 1, attribute is a list and None is not a valid list
        # If lower bound > 0, attribute must have a value, so None is unacceptable
        if value is None:
            return None
        if isinstance(value, str):
            value = dateutil.parser.parse(value)
        if not isinstance(value, datetime.datetime):
            raise TypeError(f'Expecting datetime, got {type(value)}')
        return rdflib.Literal(value)

    def to_user(self, value):
        return dateutil.parser.parse(value)


class DateTimeSingletonProperty(DateTimePropertyMixin, SingletonProperty):

    def __init__(self, property_owner: Any, property_uri: str,
                 lower_bound: int, upper_bound: int,
                 validation_rules: Optional[List] = None,
                 initial_value: Optional[str] = None):
        super().__init__(property_owner, property_uri,
                         lower_bound, upper_bound, validation_rules)
        if initial_value is not None:
            self.set(initial_value)


def DateTimeProperty(property_owner: Any, property_uri: str,
                     lower_bound: int, upper_bound: Union[int, float],
                     validation_rules: Optional[List] = None,
                     initial_value: Optional[Union[int, List[int]]] = None) -> Property:
    if upper_bound == 1:
        return DateTimeSingletonProperty(property_owner, property_uri,
                                         lower_bound, upper_bound,
                                         validation_rules, initial_value)
    raise ValueError('Upper bound > 1 not handled yet')
