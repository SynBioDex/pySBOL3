import math
from typing import List, Any

from . import *


class Interface(Identified):
    """The Interface class is a way of explicitly specifying the interface
    of a Component.

    """

    def __init__(self, *, inputs: List[str] = None, outputs: List[str] = None,
                 nondirectionals: List[str] = None, name: str = None,
                 description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_INTERFACE) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        self.inputs = ReferencedObject(self, SBOL_INPUT, 0, math.inf,
                                       initial_value=inputs)
        self.outputs = ReferencedObject(self, SBOL_OUTPUT, 0, math.inf,
                                        initial_value=outputs)
        self.nondirectionals = ReferencedObject(self, SBOL_NONDIRECTIONAL,
                                                0, math.inf,
                                                initial_value=nondirectionals)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_interface` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_interface method
        :return: Whatever `visitor.visit_interface` returns
        :rtype: Any

        """
        visitor.visit_interface(self)


def build_interface(identity: str, *, type_uri: str = SBOL_INTERFACE) -> SBOLObject:
    return Interface(identity=identity, type_uri=type_uri)


Document.register_builder(SBOL_INTERFACE, build_interface)
