import abc
import math
from typing import Union

from . import *
from .om_prefix import Prefix


class Unit(TopLevel, abc.ABC):
    """om:Unit is an abstract base class.

    See Appendix A Section A.2 of the SBOL 3.0 specificiation.
    """

    def __init__(self, name: str, symbol: str, label: str,
                 type_uri: str) -> None:
        super().__init__(name, type_uri)
        self.symbol = TextProperty(self, OM_SYMBOL, 1, 1,
                                   initial_value=symbol)
        self.alternative_symbols = TextProperty(self, OM_ALTERNATIVE_SYMBOL,
                                                0, math.inf)
        self.label = TextProperty(self, OM_LABEL, 1, 1,
                                  initial_value=label)
        self.alternative_labels = TextProperty(self, OM_ALTERNATIVE_LABEL,
                                               0, math.inf)
        self.comment = TextProperty(self, OM_COMMENT, 0, 1)
        self.long_comment = TextProperty(self, OM_LONG_COMMENT, 0, 1)


class Measure(Identified):

    def __init__(self, value: float, unit: str,
                 *, name: str = None,
                 type_uri: str = OM_MEASURE) -> None:
        super().__init__(name, type_uri)
        self.value = FloatProperty(self, OM_HAS_NUMERICAL_VALUE, 1, 1,
                                   initial_value=value)
        self.types = URIProperty(self, SBOL_TYPE, 0, math.inf)
        self.unit = URIProperty(self, OM_HAS_UNIT, 1, 1,
                                initial_value=unit)
        self.validate()


def build_measure(name: str, *, type_uri: str = OM_MEASURE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Measure(1.0, missing, name=name, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_HAS_NUMERICAL_VALUE] = []
    obj._properties[OM_HAS_UNIT] = []
    return obj


Document.register_builder(OM_MEASURE, build_measure)


class SingularUnit(Unit):

    def __init__(self, name: str, symbol: str, label: str,
                 *, type_uri: str = OM_SINGULAR_UNIT) -> None:
        super().__init__(name, symbol, label, type_uri)
        self.unit = ReferencedObject(self, OM_HAS_UNIT, 0, 1)
        self.factor = FloatProperty(self, OM_HAS_FACTOR, 0, 1)
        self.validate()


def build_singular_unit(name: str, *, type_uri: str = OM_SINGULAR_UNIT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = SingularUnit(name, missing, missing, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    return obj


Document.register_builder(OM_SINGULAR_UNIT, build_singular_unit)


class PrefixedUnit(Unit):

    def __init__(self, name: str, symbol: str, label: str,
                 unit: Union[Unit, str],
                 prefix: Union[Prefix, str],
                 *, type_uri: str = OM_PREFIXED_UNIT) -> None:
        super().__init__(name, symbol, label, type_uri)
        self.unit = ReferencedObject(self, OM_HAS_UNIT, 1, 1,
                                     initial_value=unit)
        self.prefix = ReferencedObject(self, OM_HAS_PREFIX, 1, 1,
                                       initial_value=prefix)
        self.validate()


def build_prefixed_unit(name: str, *, type_uri: str = OM_PREFIXED_UNIT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = PrefixedUnit(name, missing, missing, missing, missing, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_UNIT] = []
    obj._properties[OM_HAS_PREFIX] = []
    return obj


Document.register_builder(OM_PREFIXED_UNIT, build_prefixed_unit)
