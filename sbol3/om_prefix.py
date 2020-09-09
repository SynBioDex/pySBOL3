import abc
import math

from . import *


class Prefix(TopLevel, abc.ABC):
    """om:Prefix is an abstract base class.

    See Appendix A Section A.2 of the SBOL 3.0 specificiation.
    """

    def __init__(self, name: str, symbol: str, label: str,
                 factor: float, type_uri: str) -> None:
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
        self.factor = FloatProperty(self, OM_HAS_FACTOR, 1, 1,
                                    initial_value=factor)


class SIPrefix(Prefix):

    def __init__(self, name: str, symbol: str, label: str,
                 factor: float, *, type_uri: str = OM_SI_PREFIX) -> None:
        super().__init__(name, symbol, label, factor, type_uri)


def build_si_prefix(name: str, *, type_uri: str = OM_SI_PREFIX) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = SIPrefix(name, missing, missing, 1.0, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_FACTOR] = []
    return obj


Document.register_builder(OM_SI_PREFIX, build_si_prefix)


class BinaryPrefix(Prefix):

    def __init__(self, name: str, symbol: str, label: str,
                 factor: float, *, type_uri: str = OM_BINARY_PREFIX) -> None:
        super().__init__(name, symbol, label, factor, type_uri)


def build_binary_prefix(name: str, *, type_uri: str = OM_BINARY_PREFIX) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = BinaryPrefix(name, missing, missing, 1.0, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_FACTOR] = []
    return obj


Document.register_builder(OM_BINARY_PREFIX, build_binary_prefix)
