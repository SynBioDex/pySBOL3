import abc
from typing import Union

from . import *

int_property = Union[IntProperty, int]


class Location(Identified, abc.ABC):

    def __init__(self, seq_or_uri: Union[Sequence, str],
                 identity: str, type_uri: str) -> None:
        super().__init__(identity, type_uri)
        self.orientation = URIProperty(self, SBOL_ORIENTATION, 0, 1)
        self.order = IntProperty(self, SBOL_ORDER, 0, 1)
        self.sequence = ReferencedObject(self, SBOL_SEQUENCES, 1, 1,
                                         initial_value=seq_or_uri)

    def validate(self) -> None:
        super().validate()
        if not self.sequence:
            raise ValidationError(f'Location {self.identity} does not have a sequence')


class Range(Location):

    def __init__(self, seq_or_uri: Union[Sequence, str], start: int, end: int,
                 *, identity: str = None, type_uri: str = SBOL_RANGE) -> None:
        super().__init__(seq_or_uri, identity, type_uri)
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


def build_range(identity: str, type_uri: str = SBOL_RANGE):
    """Used by Document to construct a Range when reading an SBOL file.
    """
    start = 1
    end = 1
    obj = Range(PYSBOL3_MISSING, start, end, identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_SEQUENCES] = []
    obj._properties[SBOL_START] = []
    obj._properties[SBOL_END] = []
    return obj


Document.register_builder(SBOL_RANGE, build_range)


class Cut(Location):

    def __init__(self, seq_or_uri: Union[Sequence, str], at: int,
                 *, identity: str = None, type_uri: str = SBOL_CUT) -> None:
        super().__init__(seq_or_uri, identity, type_uri)
        self.at: int_property = IntProperty(self, SBOL_START, 1, 1,
                                            initial_value=at)
        self.validate()

    def validate(self) -> None:
        super().validate()
        if self.at < 0:
            raise ValidationError('At must be >= 0')


def build_cut(identity: str, type_uri: str = SBOL_CUT):
    """Used by Document to construct a Cut when reading an SBOL file.
    """
    at = 0
    obj = Cut(PYSBOL3_MISSING, at, identity=identity, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[SBOL_SEQUENCES] = []
    obj._properties[SBOL_START] = []
    return obj


Document.register_builder(SBOL_CUT, build_cut)


class EntireSequence(Location):

    def __init__(self, seq_or_uri: Union[Sequence, str],
                 *, identity: str = None,
                 type_uri: str = SBOL_ENTIRE_SEQUENCE) -> None:
        super().__init__(seq_or_uri, identity, type_uri)
        self.validate()


def build_entire_sequence(identity: str, type_uri: str = SBOL_ENTIRE_SEQUENCE):
    """Used by Document to construct an EntireSequence when reading an SBOL file.
    """
    obj = EntireSequence(PYSBOL3_MISSING, identity=identity, type_uri=type_uri)
    obj._properties[SBOL_SEQUENCES] = []
    return obj


Document.register_builder(SBOL_ENTIRE_SEQUENCE, EntireSequence)
