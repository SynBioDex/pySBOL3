import abc
from typing import Union

from . import *

int_property = Union[IntProperty, int]


class Location(Identified, abc.ABC):

    def __init__(self, name: str, type_uri: str) -> None:
        super().__init__(name, type_uri)
        self.orientation = URIProperty(self, SBOL_ORIENTATION, 0, 1)
        self.order = IntProperty(self, SBOL_ORDER, 0, 1)


class Range(Location):

    @staticmethod
    def _builder(identity_uri: str, type_uri: str = SBOL_RANGE):
        """Used by Document to construct a SubComponent when reading an SBOL file.
        """
        start = 1
        end = 1
        return Range(identity_uri, start, end, type_uri=type_uri)

    def __init__(self, name: str, start: int, end: int,
                 *, type_uri: str = SBOL_RANGE, ) -> None:
        super().__init__(name, type_uri)
        self.start: int_property = IntProperty(self, SBOL_START, 1, 1,
                                               initial_value=start)
        self.end: int_property = IntProperty(self, SBOL_END, 1, 1,
                                             initial_value=end)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if self.start < 1:
            raise ValidationError('Start must be greater than 0')
        if self.end < 1:
            raise ValidationError('Start must be greater than 0')
        if self.end < self.start:
            raise ValidationError('End must be >= start')


Document.register_builder(SBOL_RANGE, Range._builder)


class Cut(Location):

    @staticmethod
    def _builder(identity_uri: str, type_uri: str = SBOL_CUT):
        """Used by Document to construct a SubComponent when reading an SBOL file.
        """
        at = 0
        return Cut(identity_uri, at, type_uri=type_uri)

    def __init__(self, name: str, at: int,
                 *, type_uri: str = SBOL_CUT) -> None:
        super().__init__(name, type_uri)
        self.at: int_property = IntProperty(self, SBOL_START, 1, 1,
                                            initial_value=at)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if self.at < 0:
            raise ValidationError('At must be >= 0')


Document.register_builder(SBOL_CUT, Cut._builder)


class EntireSequence(Location):

    def __init__(self, name: str, *,
                 type_uri: str = SBOL_ENTIRE_SEQUENCE) -> None:
        super().__init__(name, type_uri)
        self.validate()


Document.register_builder(SBOL_ENTIRE_SEQUENCE, EntireSequence)
