from __future__ import annotations

import copy
import math
import posixpath
import uuid
from typing import Dict, Callable, Optional
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

    def copy(self, target_doc=None, target_namespace=None):
        new_obj = super().copy(target_doc=target_doc, target_namespace=target_namespace)
        # Need to set `document` on all children recursively. That's what happens when
        # you assign to the `document` property of an Identified
        new_obj.document = target_doc
        # Comply with the contract of super.copy()
        return new_obj


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
