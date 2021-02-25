import abc
from typing import Union, List

from . import *

from .om_unit import Unit


class CompoundUnit(Unit, abc.ABC):
    """As adopted by SBOL, om:CompoundUnit is an abstract class that is
    extended by other classes to describe units of measure that can be
    represented as combinations of multiple other units of measure.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 type_uri: str,
                 *, alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None) -> None:
        super().__init__(symbol=symbol, label=label,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)


class UnitMultiplication(CompoundUnit):
    """The purpose of the om:UnitMultiplication class is to describe a
    unit of measure that is the multiplication of two other units of
    measure.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 term1: Union[Unit, str], term2: Union[Unit, str],
                 *, alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = OM_UNIT_MULTIPLICATION) -> None:
        super().__init__(symbol=symbol, label=label,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.term1 = ReferencedObject(self, OM_HAS_TERM1, 1, 1,
                                      initial_value=term1)
        self.term2 = ReferencedObject(self, OM_HAS_TERM2, 1, 1,
                                      initial_value=term2)


def build_unit_multiplication(identity: str,
                              *, type_uri: str = OM_UNIT_MULTIPLICATION) -> SBOLObject:
    obj = UnitMultiplication(identity=identity, type_uri=type_uri,
                             symbol=PYSBOL3_MISSING, label=PYSBOL3_MISSING,
                             term1=PYSBOL3_MISSING, term2=PYSBOL3_MISSING)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_TERM1] = []
    obj._properties[OM_HAS_TERM2] = []
    return obj


Document.register_builder(OM_UNIT_MULTIPLICATION, build_unit_multiplication)


class UnitDivision(CompoundUnit):
    """The purpose of the om:UnitDivision class is to describe a unit of
    measure that is the division of one unit of measure by another.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 numerator: Union[Unit, str], denominator: Union[Unit, str],
                 *, alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = OM_UNIT_DIVISION) -> None:
        super().__init__(symbol=symbol, label=label,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.numerator = ReferencedObject(self, OM_HAS_NUMERATOR, 1, 1,
                                          initial_value=numerator)
        self.denominator = ReferencedObject(self, OM_HAS_DENOMINATOR, 1, 1,
                                            initial_value=denominator)


def build_unit_division(identity: str,
                        *, type_uri: str = OM_UNIT_DIVISION) -> SBOLObject:
    obj = UnitDivision(identity=identity, type_uri=type_uri,
                       symbol=PYSBOL3_MISSING, label=PYSBOL3_MISSING,
                       numerator=PYSBOL3_MISSING, denominator=PYSBOL3_MISSING)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_NUMERATOR] = []
    obj._properties[OM_HAS_DENOMINATOR] = []
    return obj


Document.register_builder(OM_UNIT_DIVISION, build_unit_division)


class UnitExponentiation(CompoundUnit):
    """The purpose of the om:UnitExponentiation class is to describe a
    unit of measure that is raised to an integer power.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 base: Union[Unit, str], exponent: int,
                 *, alternative_symbols: List[str] = None,
                 alternative_labels: List[str] = None,
                 comment: str = None,
                 long_comment: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = OM_UNIT_EXPONENTIATION) -> None:
        super().__init__(symbol=symbol, label=label,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.base = ReferencedObject(self, OM_HAS_BASE, 1, 1,
                                     initial_value=base)
        self.exponent = IntProperty(self, OM_HAS_EXPONENT, 1, 1,
                                    initial_value=exponent)


def build_unit_exponentiation(identity: str,
                              *, type_uri: str = OM_UNIT_EXPONENTIATION) -> SBOLObject:
    obj = UnitExponentiation(identity=identity, type_uri=type_uri,
                             symbol=PYSBOL3_MISSING, label=PYSBOL3_MISSING,
                             base=PYSBOL3_MISSING, exponent=1)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_BASE] = []
    obj._properties[OM_HAS_EXPONENT] = []
    return obj


Document.register_builder(OM_UNIT_EXPONENTIATION, build_unit_exponentiation)
