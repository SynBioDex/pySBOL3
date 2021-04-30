from typing import Union, List, Any

from . import *


class Implementation(TopLevel):
    """An Implementation represents a realized instance of a Component,
    such a sample of DNA resulting from fabricating a genetic design
    or an aliquot of a specified reagent. Importantly, an
    Implementation can be associated with a laboratory sample that was
    already built, or that is planned to be built in the future. An
    Implementation can also represent virtual and simulated
    instances. An Implementation may be linked back to its original
    design using the prov:wasDerivedFrom property inherited from the
    Identified superclass. An Implementation may also link to a
    Component that specifies its realized structure and/or
    function.

    """

    def __init__(self, identity: str,
                 *, built: Union[Component, str] = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None, generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_IMPLEMENTATION) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.built = ReferencedObject(self, SBOL_BUILT, 0, 1,
                                      initial_value=built)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_implementation` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_implementation method
        :return: Whatever `visitor.visit_implementation` returns
        :rtype: Any

        """
        visitor.visit_implementation(self)


Document.register_builder(SBOL_IMPLEMENTATION, Implementation)
