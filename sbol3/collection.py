import math
from typing import List, Any

from . import *


class Collection(TopLevel):
    """The Collection class is a class that groups together a set of
    TopLevel objects that have something in common.

    Some examples of Collection objects:

    * Results of a query to find all Component objects in a repository
      that function as promoters.
    * A set of Component objects representing a library of genetic
      logic gates.
    * A "parts list" for Component with a complex design, containing
      both that component and all of the Component, Sequence, and
      Model objects used to provide its full specification.

    """

    def __init__(self, identity: str,
                 *, members: List[str] = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_COLLECTION) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.members = ReferencedObject(self, SBOL_MEMBER, 0, math.inf,
                                        initial_value=members)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_collection` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_collection method
        :return: Whatever `visitor.visit_collection` returns
        :rtype: Any

        """
        visitor.visit_collection(self)


class Experiment(Collection):
    """The purpose of the Experiment class is to aggregate
    ExperimentalData objects for subsequent analysis, usually in
    accordance with an experimental design. Namely, the member
    properties of an Experiment MUST refer to ExperimentalData
    objects.

    """

    def __init__(self, identity: str,
                 *, members: List[str] = None,
                 namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 type_uri: str = SBOL_EXPERIMENT) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         members=members, namespace=namespace,
                         attachments=attachments, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_experiment` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_experiment method
        :return: Whatever `visitor.visit_experiment` returns
        :rtype: Any

        """
        visitor.visit_experiment(self)


Document.register_builder(SBOL_COLLECTION, Collection)
Document.register_builder(SBOL_EXPERIMENT, Experiment)
