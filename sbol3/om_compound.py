import abc
from typing import Union

from . import *

from .om_unit import Unit


class CompoundUnit(Unit, abc.ABC):

    def __init__(self, identity: str, symbol: str, label: str,
                 type_uri: str) -> None:
        super().__init__(identity, symbol, label, type_uri)


class UnitMultiplication(CompoundUnit):

    def __init__(self, identity: str, symbol: str, label: str,
                 term1: Union[Unit, str], term2: Union[Unit, str],
                 *, type_uri: str = OM_UNIT_MULTIPLICATION) -> None:
        super().__init__(identity, symbol, label, type_uri)
        self.term1 = ReferencedObject(self, OM_HAS_TERM1, 1, 1,
                                      initial_value=term1)
        self.term2 = ReferencedObject(self, OM_HAS_TERM2, 1, 1,
                                      initial_value=term2)
        self.validate()


def build_unit_multiplication(identity: str,
                              *, type_uri: str = OM_UNIT_MULTIPLICATION) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = UnitMultiplication(identity, missing, missing, missing, missing,
                             type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_TERM1] = []
    obj._properties[OM_HAS_TERM2] = []
    return obj


Document.register_builder(OM_UNIT_MULTIPLICATION, build_unit_multiplication)


class UnitDivision(CompoundUnit):

    def __init__(self, identity: str, symbol: str, label: str,
                 numerator: Union[Unit, str], denominator: Union[Unit, str],
                 *, type_uri: str = OM_UNIT_DIVISION) -> None:
        super().__init__(identity, symbol, label, type_uri)
        self.numerator = ReferencedObject(self, OM_HAS_NUMERATOR, 1, 1,
                                          initial_value=numerator)
        self.denominator = ReferencedObject(self, OM_HAS_DENOMINATOR, 1, 1,
                                            initial_value=denominator)
        self.validate()


def build_unit_division(identity: str,
                        *, type_uri: str = OM_UNIT_DIVISION) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = UnitDivision(identity, missing, missing, missing, missing, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_NUMERATOR] = []
    obj._properties[OM_HAS_DENOMINATOR] = []
    return obj


Document.register_builder(OM_UNIT_DIVISION, build_unit_division)


class UnitExponentiation(CompoundUnit):

    def __init__(self, identity: str, symbol: str, label: str,
                 base: Union[Unit, str], exponent: int,
                 *, type_uri: str = OM_UNIT_EXPONENTIATION) -> None:
        super().__init__(identity, symbol, label, type_uri)
        self.base = ReferencedObject(self, OM_HAS_BASE, 1, 1,
                                     initial_value=base)
        self.exponent = IntProperty(self, OM_HAS_EXPONENT, 1, 1,
                                    initial_value=exponent)
        self.validate()


def build_unit_exponentiation(identity: str,
                              *, type_uri: str = OM_UNIT_EXPONENTIATION) -> SBOLObject:
    missing = PYSBOL3_MISSING
    obj = UnitExponentiation(identity, missing, missing, missing, 1, type_uri=type_uri)
    # Remove the dummy values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_BASE] = []
    obj._properties[OM_HAS_EXPONENT] = []
    return obj


Document.register_builder(OM_UNIT_EXPONENTIATION, build_unit_exponentiation)
