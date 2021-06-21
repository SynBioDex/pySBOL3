import copy
import math
import posixpath
from typing import List, Dict, Callable, Union
from urllib.parse import urlparse

from . import *


class TopLevel(Identified):
    """TopLevel is an abstract class that is extended by any Identified
    class that can be found at the top level of an SBOL document or
    file. In other words, TopLevel objects are not nested inside any
    other object via composite aggregation. Instead of nesting,
    composite TopLevel objects refer to subordinate TopLevel objects
    by their URIs using shared aggregation.

    """

    def __init__(self, identity: str, type_uri: str,
                 *, namespace: str = None,
                 attachments: List[str] = None,
                 name: str = None, description: str = None,
                 derived_from: List[str] = None,
                 generated_by: List[str] = None,
                 measures: List[SBOLObject] = None) -> None:
        # Check identity, which is required for a TopLevel
        # More checking on identity happens in Identified, but Identified
        # does not require an identity, only TopLevel does.
        if not identity or not isinstance(identity, str):
            raise ValueError('Identity must be a non-empty string')
        super().__init__(identity=identity, type_uri=type_uri,
                         name=name, description=description,
                         derived_from=derived_from, generated_by=generated_by,
                         measures=measures)
        if namespace is None:
            namespace = TopLevel.default_namespace(namespace, self.identity)
        self.namespace = URIProperty(self, SBOL_NAMESPACE, 1, 1,
                                     initial_value=namespace)
        self.attachments = ReferencedObject(self, SBOL_HAS_ATTACHMENT, 0, math.inf,
                                            initial_value=attachments)

    @staticmethod
    def default_namespace(namespace: Union[None, str], identity: str) -> str:
        # short circuit if a namespace is set
        if namespace is not None:
            return namespace
        # Try using the default namespace if set
        namespace = get_namespace()
        if namespace is None:
            # No default namespace was defined
            # Try parsing the identity as a URL
            parsed = urlparse(identity)
            if parsed.scheme and parsed.netloc and parsed.path:
                # This is a URL
                # Reverse index to drop the displayId and use the rest
                # for the namespace
                delim = posixpath.sep
                if '#' in identity:
                    delim = '#'
                namespace = identity[:identity.rindex(delim)]
        if namespace is None:
            # TODO: what should we do here? We haven't been able to determine
            #       a namespace. But in the case where we're loading a file
            #       that's probably ok. We don't want that loading to fail.
            pass
        return namespace

    def validate_identity(self, report: ValidationReport) -> None:
        # TODO: See section 5.1 for rules about identity for TopLevel
        pass

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        return report

    def _reparent_child_objects(self) -> None:
        for k, v in self.__dict__.items():
            if not isinstance(v, Property):
                continue
            if v.property_uri not in self._owned_objects:
                continue
            old_list = self._owned_objects[v.property_uri]
            if len(old_list) == 0:
                continue
            self._owned_objects[v.property_uri] = []
            if isinstance(v, ListProperty):
                setattr(self, k, old_list)
            else:
                setattr(self, k, old_list[0])

    def clone(self, new_identity: str) -> 'TopLevel':
        obj = copy.deepcopy(self)
        identity_map = {self.identity: obj}
        # Set identity of new object
        obj._identity = obj._make_identity(new_identity)
        # Set display_id of new object
        obj._display_id = obj._extract_display_id(obj._identity)
        # Drop the document pointer
        obj.document = None

        # Erase the identity and display_id of the entire tree
        obj.traverse(make_erase_identity_traverser(identity_map))

        # Now remove and re-add all child objects to update
        # their identities
        obj._reparent_child_objects()

        # TODO: Now remap any properties that reference old
        #       identities in the identity_map
        obj.traverse(make_update_references_traverser(identity_map))
        return obj


def make_erase_identity_traverser(identity_map: Dict[str, Identified])\
        -> Callable[[Identified], None]:
    def erase_identity_traverser(x):
        if isinstance(x, TopLevel):
            return
        identity_map[x.identity] = x
        x._identity = None
        x._display_id = None
        x.document = None
    return erase_identity_traverser


def make_update_references_traverser(identity_map: Dict[str, Identified])\
        -> Callable[[Identified], None]:
    def update_references_traverser(x):
        # Use the identity map to update references.
        # References to objects outside of the object
        # being cloned will be left as is.
        for k, v in x.__dict__.items():
            if not isinstance(v, Property):
                continue
            if v.property_uri not in x._properties:
                continue
            items = x._properties[v.property_uri]
            for i in range(len(items)):
                str_item = str(items[i])
                if str_item in identity_map:
                    new_reference = identity_map[str_item].identity
                    # The item is probably an rdflib.URIRef. We take
                    # the type of the item and use that type to
                    # construct a new instance of the same type.
                    # Hacky? yes, and it seems to work
                    constructor = type(items[i])
                    items[i] = constructor(new_reference)
    return update_references_traverser
