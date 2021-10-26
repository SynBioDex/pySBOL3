from __future__ import annotations
import abc
import math
from typing import Union, List, Any, Optional

from . import *
from .om_prefix import Prefix
from .typing import *


class Unit(CustomTopLevel, abc.ABC):
    """As adopted by SBOL, om:Unit is an abstract class that is extended
    by other classes to describe units of measure using a shared set
    of properties.

    See Appendix A Section A.2 of the SBOL 3.0 specificiation.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 type_uri: str,
                 *, alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.symbol = TextProperty(self, OM_SYMBOL, 1, 1,
                                   initial_value=symbol)
        self.alternative_symbols = TextProperty(self, OM_ALTERNATIVE_SYMBOL,
                                                0, math.inf,
                                                initial_value=alternative_symbols)
        self.label = TextProperty(self, OM_LABEL, 1, 1,
                                  initial_value=label)
        self.alternative_labels = TextProperty(self, OM_ALTERNATIVE_LABEL,
                                               0, math.inf,
                                               initial_value=alternative_labels)
        self.comment = TextProperty(self, OM_COMMENT, 0, 1,
                                    initial_value=comment)
        self.long_comment = TextProperty(self, OM_LONG_COMMENT, 0, 1,
                                         initial_value=long_comment)


class Measure(CustomIdentified):
    """The purpose of the om:Measure class is to link a numerical value to
    a om:Unit.

    """

    def __init__(self, value: float, unit: str,
                 *, types: Optional[str, list[str]] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = OM_MEASURE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.value = FloatProperty(self, OM_HAS_NUMERICAL_VALUE, 1, 1,
                                   initial_value=value)
        self.types: uri_list = URIProperty(self, SBOL_TYPE, 0, math.inf,
                                           initial_value=types)
        self.unit: uri_singleton = URIProperty(self, OM_HAS_UNIT, 1, 1,
                                               initial_value=unit)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_measure` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_measure method
        :return: Whatever `visitor.visit_measure` returns
        :rtype: Any

        """
        visitor.visit_measure(self)


def build_measure(identity: str, *, type_uri: str = OM_MEASURE) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = Measure(1.0, missing, identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[OM_HAS_NUMERICAL_VALUE] = []
    obj._properties[OM_HAS_UNIT] = []
    return obj


Document.register_builder(OM_MEASURE, build_measure)


class SingularUnit(Unit):
    """The purpose of the om:SingularUnit class is to describe a unit of
    measure that is not explicitly represented as a combination of
    multiple units, but could be equivalent to such a
    representation. For example, a joule is considered to be a
    om:SingularUnit, but it is equivalent to the multiplication of a
    newton and a meter.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 *, unit: str = None, factor: float = None,
                 alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = OM_SINGULAR_UNIT) -> None:
        super().__init__(symbol=symbol, label=label,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.unit = ReferencedObject(self, OM_HAS_UNIT, 0, 1,
                                     initial_value=unit)
        self.factor = FloatProperty(self, OM_HAS_FACTOR, 0, 1,
                                    initial_value=factor)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_singular_unit` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_singular_unit method
        :return: Whatever `visitor.visit_singular_unit` returns
        :rtype: Any

        """
        visitor.visit_singular_unit(self)


def build_singular_unit(identity: str,
                        *, type_uri: str = OM_SINGULAR_UNIT) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = SingularUnit(symbol=missing, label=missing,
                       identity=identity, type_uri=type_uri)
    # Remove the placeholder values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    return obj


Document.register_builder(OM_SINGULAR_UNIT, build_singular_unit)


class PrefixedUnit(Unit):
    """The purpose of the om:PrefixedUnit class is to describe a unit of
    measure that is the multiplication of another unit of measure and
    a factor represented by a standard prefix such as “milli,”
    “centi,” “kilo,” etc.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 unit: Union[Unit, str],
                 prefix: Union[Prefix, str],
                 *, alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = OM_PREFIXED_UNIT) -> None:
        super().__init__(symbol=symbol, label=label,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.unit = ReferencedObject(self, OM_HAS_UNIT, 1, 1,
                                     initial_value=unit)
        self.prefix = ReferencedObject(self, OM_HAS_PREFIX, 1, 1,
                                       initial_value=prefix)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_prefixed_unit` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_prefixed_unit method
        :return: Whatever `visitor.visit_prefixed_unit` returns
        :rtype: Any

        """
        visitor.visit_prefixed_unit(self)


def build_prefixed_unit(identity: str,
                        *, type_uri: str = OM_PREFIXED_UNIT) -> SBOLObject:
    obj = PrefixedUnit(identity=identity, type_uri=type_uri,
                       symbol=PYSBOL3_MISSING, label=PYSBOL3_MISSING,
                       unit=PYSBOL3_MISSING, prefix=PYSBOL3_MISSING)
    # Remove the placeholder values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_UNIT] = []
    obj._properties[OM_HAS_PREFIX] = []
    return obj


Document.register_builder(OM_PREFIXED_UNIT, build_prefixed_unit)
