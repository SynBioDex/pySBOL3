from __future__ import annotations

import copy
import math
import posixpath
import urllib.parse
import uuid
import warnings
from typing import Dict, Callable, Optional, Any
import typing

from . import *
from .typing import *


class TopLevel(Identified):
    """TopLevel is an abstract class that is extended by any Identified
    class that can be found at the top level of an SBOL document or
    file. In other words, TopLevel objects are not nested inside any
    other object via composite aggregation. Instead of nesting,
    composite TopLevel objects refer to subordinate TopLevel objects
    by their URIs using shared aggregation.

    """

    def __init__(self, identity: str, type_uri: str,
                 *, namespace: Optional[str] = None,
                 attachments: Optional[refobj_list_arg] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 derived_from: Optional[Union[str, typing.Sequence[str]]] = None,
                 generated_by: Optional[refobj_list_arg] = None,
                 measures: Optional[ownedobj_list_arg] = None) -> None:
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
        if self._is_url(self.identity) and not self.identity.startswith(namespace):
            msg = 'Namespace must be a prefix of identity.'
            msg += f' Namespace {namespace} is not a prefix of {self.identity}.'
            raise ValueError(msg)
        self.namespace = URIProperty(self, SBOL_NAMESPACE, 1, 1,
                                     initial_value=namespace)
        self.attachments = ReferencedObject(self, SBOL_HAS_ATTACHMENT, 0, math.inf,
                                            initial_value=attachments)

    @staticmethod
    def default_namespace(namespace: Union[None, str], identity: str) -> str:
        # short circuit if a namespace is set
        if namespace is not None:
            return namespace
        default_namespace = get_namespace()
        # If identity is a uuid, don't bother with namespaces
        try:
            # If it is a UUID, accept it as the identity
            uuid.UUID(identity)
            return default_namespace or PYSBOL3_DEFAULT_NAMESPACE
        except ValueError:
            pass
        # If default namespace is a prefix of identity, use it for the namespace
        if default_namespace and identity.startswith(default_namespace):
            return default_namespace
        # Identity does not start with the default namespace then
        # heuristically determine the namespace. We use a greedy
        # algorithm by assuming there is no local path, and that
        # everything other than the display_id is the namespace.
        delim = posixpath.sep
        if '#' in identity:
            delim = '#'
        namespace = identity[:identity.rindex(delim)]
        return namespace

    def validate_identity(self, report: ValidationReport) -> None:
        # TODO: See section 5.1 for rules about identity for TopLevel
        pass

    def _validate_namespace(self, report: ValidationReport) -> None:
        # Rule sbol3-10301: If the URI for the TopLevel object is a URL,
        #   then the URI of the hasNamespace property MUST prefix match that URL.
        #   Reference: Section 6.2
        #
        # See https://github.com/SynBioDex/pySBOL3/issues/277
        # See https://github.com/SynBioDex/pySBOL3/issues/278
        if not self.namespace:
            # SHACL rules will handle a missing namespace
            return
        if self._is_url(self.identity):
            if not self.identity.startswith(self.namespace):
                msg = f'The namespace {self.namespace} is not a prefix'
                msg += f' of the identity {self.identity}'
                report.addError(self.identity, 'sbol3-10301', msg)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        report = super().validate(report)
        self._validate_namespace(report)
        return report

    def remove_from_document(self):
        my_doc = self.document
        super().remove_from_document()
        if my_doc is not None:
            my_doc.remove_object(self)

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

    def set_identity(self, new_identity: str) -> Any:
        """Sets the identity of the object.

        USE WITH EXTREME CAUTION!

        This method can break a tree of objects, and invalid a document.
        Only use this method if you understand the ramifications of
        changing the identity of a top level object.

        :param new_identity: the new identity
        :return: Nothing
        """
        self._identity = self._make_identity(new_identity)
        # Set display_id of new object
        self._display_id = self._extract_display_id(self._identity)

    def clone(self, new_identity: str = None) -> 'TopLevel':
        obj = copy.deepcopy(self)
        identity_map = {self.identity: obj}
        # Set identity of new object
        if new_identity is not None:
            obj.set_identity(new_identity)
        # Drop the document pointer
        obj.document = None

        obj.update_all_dependents(identity_map)
        return obj

    def update_all_dependents(self, identity_map: dict[str, Identified]) -> Any:
        """Update all dependent objects based on the provided identity map.

        Dependent objects are reparented and references are updated according
        to the identities and objects in `identity_map`.

        USE WITH CAUTION!

        :param identity_map: map of identity to Identified
        :return: Nothing
        """
        # Erase the identity and display_id of the entire tree
        self.traverse(make_erase_identity_traverser(identity_map))
        # Now remove and re-add all child objects to update
        # their identities
        self._reparent_child_objects()
        # Now remap any properties that reference old identities in the
        # identity_map
        self.traverse(make_update_references_traverser(identity_map))

    def copy(self, target_doc=None, target_namespace=None):
        # Delete this method in v1.1
        warnings.warn('Use sbol3.copy() instead', DeprecationWarning)
        new_obj = super().copy(target_doc=target_doc, target_namespace=target_namespace)
        # Need to set `document` on all children recursively. That's what happens when
        # you assign to the `document` property of an Identified
        new_obj.document = target_doc
        # Comply with the contract of super.copy()
        return new_obj

    def split_identity(self) -> tuple[str, str, str]:
        """Split this object's identity into three components:
        namespace, path, and display_id.

        :return: A tuple of namespace, path, and display_id
        """
        parsed = urllib.parse.urlparse(self.identity)
        path_elements = parsed.path.split('/')
        if path_elements[-1] != self.display_id:
            msg = f'Mismatch between identity {self.identity}'
            msg += f' and display_id {self.display_id}'
            raise ValueError(msg)
        # pop the display_id off the end
        path_elements.pop()
        # Make the parsed URL elements into a list so we can use urlunparse
        url_elements = list(parsed)
        path_idx = 2
        # Start with an empty path
        url_elements[path_idx] = ''
        while urllib.parse.urlunparse(url_elements) != self.namespace:
            url_elements[path_idx] = posixpath.join(url_elements[path_idx],
                                                    path_elements.pop(0))
        if path_elements:
            path = posixpath.join(*path_elements)
        else:
            path = ''
        return self.namespace, path, self.display_id


def make_erase_identity_traverser(identity_map: Dict[str, Identified])\
        -> Callable[[Identified], None]:
    def erase_identity_traverser(x):
        if isinstance(x, TopLevel):
            return
        identity_map[x.identity] = x
        x._identity = None
        # x._display_id = None
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
