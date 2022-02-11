import math
from typing import Union, List, Any, Optional

from . import *
# Feature is not exported
from .feature import Feature
from .typing import uri_singleton


class SubComponent(Feature):
    """The SubComponent class can be used to specify structural
    hierarchy. For example, the Component of a gene might contain four
    SubComponent objects: a promoter, RBS, CDS, and terminator, each
    linked to a Component that provides the complete definition. In
    turn, the Component of the promoter SubComponent might itself
    contain SubComponent objects defining various operator sites, etc.

    """

    def __init__(self, instance_of: Union[Identified, str],
                 *, role_integration: Optional[str] = None,
                 locations: Union[Location, List[Location]] = None,
                 source_locations: Union[Location, List[Location]] = None,
                 roles: List[str] = None, orientation: str = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None,
                 identity: str = None,
                 type_uri: str = SBOL_SUBCOMPONENT) -> None:
        super().__init__(identity=identity, type_uri=type_uri,
                         roles=roles, orientation=orientation, name=name,
                         description=description, derived_from=derived_from,
                         generated_by=generated_by, measures=measures)
        self.role_integration: uri_singleton = URIProperty(self, SBOL_ROLE, 0, 1,
                                                           initial_value=role_integration)
        self.instance_of = ReferencedObject(self, SBOL_INSTANCE_OF, 1, 1,
                                            initial_value=instance_of)
        self.source_locations = OwnedObject(self, SBOL_SOURCE_LOCATION, 0, math.inf,
                                            initial_value=source_locations,
                                            type_constraint=Location)
        self.locations = OwnedObject(self, SBOL_LOCATION, 0, math.inf,
                                     initial_value=locations,
                                     type_constraint=Location)

    def accept(self, visitor: Any) -> Any:
        """Invokes `visit_sub_component` on `visitor` with `self` as the only
        argument.

        :param visitor: The visitor instance
        :type visitor: Any
        :raises AttributeError: If visitor lacks a visit_sub_component method
        :return: Whatever `visitor.visit_sub_component` returns
        :rtype: Any

        """
        visitor.visit_sub_component(self)


def build_subcomponent(identity: str, type_uri: str = SBOL_SUBCOMPONENT) -> Identified:
    """Used by Document to construct a SubComponent when reading an SBOL file.
    """
    missing = PYSBOL3_MISSING
    obj = SubComponent(missing, identity=identity, type_uri=type_uri)
    obj._properties[SBOL_INSTANCE_OF] = []
    return obj


Document.register_builder(SBOL_SUBCOMPONENT, build_subcomponent)
