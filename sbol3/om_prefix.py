import abc
import math
from typing import List, Any

from . import *


class Prefix(CustomTopLevel, abc.ABC):
    """As adopted by SBOL, om:Prefix is an abstract class that is extended
    by other classes to describe factors that are commonly represented
    by standard unit prefixes. For example, the factor 10**−3 is
    represented by the standard unit prefix "milli".

    See Appendix A Section A.2 of the SBOL 3.0 specificiation.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 factor: float, type_uri: str,
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
        self.factor = FloatProperty(self, OM_HAS_FACTOR, 1, 1,
                                    initial_value=factor)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        if not self.symbol:
            message = 'Prefix must contain a symbol'
            report.addError(self.identity, None, message)
        if not self.label:
            message = 'Prefix must contain a label'
            report.addError(self.identity, None, message)
        if not self.factor:
            message = 'Prefix must contain a factor'
            report.addError(self.identity, None, message)
        return report


class SIPrefix(Prefix):
    """The purpose of the om:SIPrefix class is to describe standard SI
    prefixes such as "milli," "centi," "kilo," etc.

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 factor: float,
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
                 type_uri: str = OM_SI_PREFIX) -> None:
        super().__init__(symbol=symbol, label=label, factor=factor,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_si_prefix` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_si_prefix method
        :return: Whatever `visitor.visit_si_prefix` returns
        :rtype: Any

        """
        visitor.visit_si_prefix(self)


def build_si_prefix(identity: str, *, type_uri: str = OM_SI_PREFIX) -> SBOLObject:
    obj = SIPrefix(identity=identity, type_uri=type_uri,
                   symbol=PYSBOL3_MISSING, label=PYSBOL3_MISSING, factor=1.0)
    # Remove the placeholder values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_FACTOR] = []
    return obj


Document.register_builder(OM_SI_PREFIX, build_si_prefix)


class BinaryPrefix(Prefix):
    """The purpose of the om:BinaryPrefix class is to describe standard
    binary prefixes such as "kibi," "mebi," "gibi," etc.  These
    prefixes commonly precede units of information such as "bit" and
    "byte."

    """

    def __init__(self, identity: str, symbol: str, label: str,
                 factor: float,
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
                 type_uri: str = OM_BINARY_PREFIX) -> None:
        super().__init__(symbol=symbol, label=label, factor=factor,
                         identity=identity, type_uri=type_uri,
                         alternative_symbols=alternative_symbols,
                         alternative_labels=alternative_labels,
                         comment=comment, long_comment=long_comment,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_binary_prefix` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_binary_prefix method
        :return: Whatever `visitor.visit_binary_prefix` returns
        :rtype: Any

        """
        visitor.visit_binary_prefix(self)


def build_binary_prefix(identity: str,
                        *, type_uri: str = OM_BINARY_PREFIX) -> SBOLObject:
    obj = BinaryPrefix(identity=identity, type_uri=type_uri,
                       symbol=PYSBOL3_MISSING, label=PYSBOL3_MISSING,
                       factor=1.0)
    # Remove the placeholder values
    obj._properties[OM_SYMBOL] = []
    obj._properties[OM_LABEL] = []
    obj._properties[OM_HAS_FACTOR] = []
    return obj


Document.register_builder(OM_BINARY_PREFIX, build_binary_prefix)
