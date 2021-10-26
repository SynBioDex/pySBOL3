import abc
from typing import Union, Any, Optional

from . import *
from .typing import uri_singleton

int_property = Union[IntProperty, int]


class Location(Identified, abc.ABC):
    """The Location class is used to represent the location of Features
    within Sequences. This class is extended by the Range, Cut, and
    EntireSequence classes

    """

    def __init__(self, sequence: Union[Sequence, str],
                 identity: str, type_uri: str,
                 *, orientation: Optional[str] = None,
                 order: int = None) -> None:
        super().__init__(identity, type_uri)
        self.orientation: uri_singleton = URIProperty(self, SBOL_ORIENTATION, 0, 1,
                                                      initial_value=orientation)
        self.order = IntProperty(self, SBOL_ORDER, 0, 1,
                                 initial_value=order)
        self.sequence = ReferencedObject(self, SBOL_SEQUENCES, 1, 1,
                                         initial_value=sequence)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if not self.sequence:
            message = f'Location {self.identity} does not have a sequence'
            report.addError(self.identity, None, message)
        return report


class Range(Location):
    """A Range object specifies a region via discrete, inclusive start and
    end positions that correspond to indices for characters in the
    elements String of a Sequence.

    Note that the index of the first location is 1, as is typical
    practice in biology, rather than 0, as is typical practice in
    computer science.

    """

    def __init__(self, sequence: Union[Sequence, str], start: int, end: int,
                 *, orientation: str = None,
                 order: int = None,
                 identity: str = None, type_uri: str = SBOL_RANGE) -> None:
        super().__init__(sequence=sequence, orientation=orientation,
                         order=order, identity=identity,
                         type_uri=type_uri)
        self.start: int_property = IntProperty(self, SBOL_START, 1, 1,
                                               initial_value=start)
        self.end: int_property = IntProperty(self, SBOL_END, 1, 1,
                                             initial_value=end)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if self.start < 1:
            message = 'Range.start must be greater than 0'
            report.addError(self.identity, 'sbol3-11401', message)
        # TODO: start must also be less than or equal to len(sequence)
        if self.end < 1:
            message = 'Range.end must be greater than 0'
            report.addError(self.identity, 'sbol3-11402', message)
        # TODO: end must also be less than or equal to len(sequence)
        if self.end < self.start:
            message = 'Range.end must be >= start'
            report.addError(self.identity, 'sbol3-11403', message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_range` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_range method
        :return: Whatever `visitor.visit_range` returns
        :rtype: Any

        """
        visitor.visit_range(self)


def build_range(identity: str, type_uri: str = SBOL_RANGE):
    """Used by Document to construct a Range when reading an SBOL file.
    """
    start = 1
    end = 1
    obj = Range(PYSBOL3_MISSING, start, end, identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_SEQUENCES] = []
    obj._properties[SBOL_START] = []
    obj._properties[SBOL_END] = []
    return obj


Document.register_builder(SBOL_RANGE, build_range)


class Cut(Location):
    """The Cut class has been introduced to enable the specification of a
    region between two discrete positions. This specification is
    accomplished using the at property, which specifies a discrete
    position that corresponds to the index of a character in the
    elements String of a Sequence (except in the case when at is equal
    to zero).

    """

    def __init__(self, sequence: Union[Sequence, str], at: int,
                 *, orientation: str = None,
                 order: int = None,
                 identity: str = None, type_uri: str = SBOL_CUT) -> None:
        super().__init__(sequence=sequence, orientation=orientation,
                         order=order, identity=identity,
                         type_uri=type_uri)
        self.at: int_property = IntProperty(self, SBOL_START, 1, 1,
                                            initial_value=at)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if self.at < 0:
            message = 'Cut property "at" must be >= 0'
            report.addError(self.identity, None, message)
        return report

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_cut` on `visitor` with `self` as the only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_cut method
        :return: Whatever `visitor.visit_cut` returns
        :rtype: Any
        """
        visitor.visit_cut(self)


def build_cut(identity: str, type_uri: str = SBOL_CUT):
    """Used by Document to construct a Cut when reading an SBOL file.
    """
    at = 0
    obj = Cut(PYSBOL3_MISSING, at, identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[SBOL_SEQUENCES] = []
    obj._properties[SBOL_START] = []
    return obj


Document.register_builder(SBOL_CUT, build_cut)


class EntireSequence(Location):
    """The EntireSequence class does not have any additional
    properties. Use of this class indicates that the linked Sequence
    describes the entirety of the Component or Feature parent of this
    Location object.

    """

    def __init__(self, sequence: Union[Sequence, str],
                 *, orientation: str = None,
                 order: int = None,
                 identity: str = None,
                 type_uri: str = SBOL_ENTIRE_SEQUENCE) -> None:
        super().__init__(sequence=sequence, orientation=orientation,
                         order=order, identity=identity,
                         type_uri=type_uri)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_entire_sequence` on `visitor` with `self` as the
        only argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_entire_sequence
                                method
        :return: Whatever `visitor.visit_entire_sequence` returns
        :rtype: Any

        """
        visitor.visit_entire_sequence(self)


def build_entire_sequence(identity: str, type_uri: str = SBOL_ENTIRE_SEQUENCE):
    """Used by Document to construct an EntireSequence when reading an SBOL file.
    """
    obj = EntireSequence(PYSBOL3_MISSING, identity=identity, type_uri=type_uri)
    obj._properties[SBOL_SEQUENCES] = []
    return obj


Document.register_builder(SBOL_ENTIRE_SEQUENCE, build_entire_sequence)
