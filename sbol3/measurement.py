import abc
import math
from typing import Union

from . import *

OM_NS = 'http://www.ontology-of-units-of-measure.org/resource/om-2/'

OM_SYMBOL = OM_NS + 'symbol'
OM_ALTERNATIVE_SYMBOLS = OM_NS + 'alternativeSymbols'
OM_LABEL = OM_NS + 'label'
OM_ALTERNATIVE_LABELS = OM_NS + 'alternativeLabels'
OM_COMMENT = OM_NS + 'comment'
OM_LONG_COMMENT = OM_NS + 'longComment'
OM_PREFIXED_UNIT = OM_NS + 'PrefixedUnit'
OM_HAS_UNIT = OM_NS + 'hasUnit'
OM_HAS_PREFIX = OM_NS + 'hasPrefix'
OM_HAS_FACTOR = OM_NS + 'hasFactor'


class Unit(TopLevel, abc.ABC):
    """om:Unit is an abstract base class.

    See Appendix A Section A.2 of the SBOL 3.0 specificiation.
    """

    def __init__(self, name: str, symbol: str, label: str,
                 type_uri: str) -> None:
        super().__init__(name, type_uri)
        self.symbol = TextProperty(self, OM_SYMBOL, 1, 1,
                                   initial_value=symbol)
        self.alternative_symbols = TextProperty(self, OM_ALTERNATIVE_SYMBOLS,
                                                0, math.inf)
        self.label = TextProperty(self, OM_LABEL, 1, 1,
                                  initial_value=label)
        self.alternative_labels = TextProperty(self, OM_ALTERNATIVE_LABELS,
                                               0, math.inf)
        self.comment = TextProperty(self, OM_COMMENT, 0, 1)
        self.long_comment = TextProperty(self, OM_LONG_COMMENT, 0, 1)


class Prefix(TopLevel, abc.ABC):
    """om:Prefix is an abstract base class.

    See Appendix A Section A.2 of the SBOL 3.0 specificiation.
    """

    def __init__(self, name: str, symbol: str, label: str,
                 factor: float, type_uri: str) -> None:
        super().__init__(name, type_uri)
        self.symbol = TextProperty(self, OM_SYMBOL, 1, 1,
                                   initial_value=symbol)
        self.alternative_symbols = TextProperty(self, OM_ALTERNATIVE_SYMBOLS,
                                                0, math.inf)
        self.label = TextProperty(self, OM_LABEL, 1, 1,
                                  initial_value=label)
        self.alternative_labels = TextProperty(self, OM_ALTERNATIVE_LABELS,
                                               0, math.inf)
        self.comment = TextProperty(self, OM_COMMENT, 0, 1)
        self.long_comment = TextProperty(self, OM_LONG_COMMENT, 0, 1)
        self.factor = FloatProperty(self, OM_HAS_FACTOR, 1, 1,
                                    initial_value=factor)


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
    obj.properties[OM_SYMBOL] = []
    obj.properties[OM_LABEL] = []
    obj.properties[OM_HAS_UNIT] = []
    obj.properties[OM_HAS_PREFIX] = []
    return obj


Document.register_builder(OM_PREFIXED_UNIT, build_prefixed_unit)
