import logging
import posixpath
import uuid
import warnings
from collections import defaultdict
from urllib.parse import urlparse
from typing import Dict, Callable, Optional, Union

from . import *


class SBOLObject:

    def __init__(self, name: str) -> None:
        self._properties = defaultdict(list)
        self._owned_objects = defaultdict(list)
        self._referenced_objects = defaultdict(list)
        # Does this need to be a property? It does not get serialized to the RDF file.
        # Could it be an attribute that gets composed on the fly? Keep it simple for
        # now, and change to a property in the future if needed.
        self._identity = SBOLObject._make_identity(name)
        self._references = []

    def __setattr__(self, name, value):
        try:
            self.__dict__[name].set(value)
        except AttributeError:
            # Attribute set does not exist
            super().__setattr__(name, value)
        except KeyError:
            # property name does not exist
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        # Call the default method
        result = super().__getattribute__(name)
        if hasattr(result, '_sbol_singleton'):
            result = result.get()
        return result

    def __eq__(self, other):
        if type(other) is str:
            return self.identity == other
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.identity)

    @staticmethod
    def _is_url(name: str) -> bool:
        parsed = urlparse(name)
        return bool(parsed.scheme and parsed.netloc and parsed.path)

    @staticmethod
    def _make_identity(name: str) -> Union[str, None]:
        """Make an identity from the given name.

        If the name is a URL, that can be the identity. Or perhaps it
        needs to start with the default URI prefix (i.e. namespace).

        If the name is not a URL, prefix it with the default URI prefix
        (namespace) and verify that the result is a valid URL.

        We do not support UUIDs, which are legal SBOL identifiers.
        """
        if name is None:
            return None
        name_is_url = SBOLObject._is_url(name)
        if name_is_url:
            return name.strip(posixpath.sep)
        try:
            # If it is a UUID, accept it as the identity
            identity_uuid = uuid.UUID(name)
            return name
        except ValueError:
            pass
        # Not a URL or a UUID, so append to the namespace
        base_uri = get_namespace()
        if base_uri is None:
            # See https://github.com/SynBioDex/pySBOL3/issues/254
            warnings.warn('Using a default namespace.'
                          ' To set a namespace use set_namespace()')
            base_uri = PYSBOL3_DEFAULT_NAMESPACE
        if base_uri.endswith('#'):
            return base_uri + name
        else:
            return posixpath.join(base_uri, name.lstrip(posixpath.sep))

    @property
    def identity(self) -> str:
        # identity is a read-only property
        return self._identity

    def identity_is_url(self) -> bool:
        return self._is_url(self.identity)

    def find(self, search_string: str) -> Optional['SBOLObject']:
        if self.identity == search_string:
            return self
        if hasattr(self, 'display_id') and self.display_id == search_string:
            return self
        for obj_list in self._owned_objects.values():
            for obj in obj_list:
                result = obj.find(search_string)
                if result is not None:
                    return result
        return None

    def _resolve_references(self, new_obj):
        resolve_references = make_resolve_references_traverser(new_obj)
        self.traverse(resolve_references)

    def copy(self, target_doc=None, target_namespace=None):

        # Delete this method in v1.1
        warnings.warn('Use sbol3.copy() instead', DeprecationWarning)

        new_uri = self.identity

        # If caller specified a target_namespace argument, then copy the object into this
        # new namespace.
        if target_namespace:

            # Map the identity of self into the target namespace
            if hasattr(self, 'identity'):
                old_uri = self.identity
                new_uri = replace_namespace(old_uri, target_namespace, self.getTypeURI())

        try:
            builder = BUILDER_REGISTER[self.type_uri]
        except KeyError:
            logging.warning(f'No builder found for {self.type_uri}; assuming {self.__class__.__name__}')
            builder = self.__class__
        new_obj = builder(**dict(identity=new_uri, type_uri=self.type_uri))

        # Copy properties
        for property_uri, value_store in self._properties.items():
            new_obj._properties[property_uri] = value_store.copy()

            # TODO: Map into new namespace

        # Assign the new object to the target Document
        if target_doc is not None:
            try:
                target_doc.add(new_obj)
            except TypeError:
                pass  # object is not TopLevel

        # When an object is simply being cloned, the value of wasDerivedFrom should be
        # copied exactly as is from self. However, when copy is being used to generate
        # a new entity, the wasDerivedFrom should point back to self.
        if self.identity == new_obj.identity:
            new_obj.derived_from = self.derived_from
        else:
            new_obj.derived_from = self.identity

        # Copy child objects recursively
        for property_uri, object_list in self._owned_objects.items():
            for o in object_list:
                o_copy = o.copy(target_doc, target_namespace)
                new_obj._owned_objects[property_uri].append(o_copy)
                o_copy.parent = self

        # After we have copied all the owned objects, copy the referenced objects
        # and attempt to resolve the references
        if target_doc:
            for property_uri, object_store in self._referenced_objects.items():
                for o in object_store:
                    referenced_obj = target_doc.find(o.identity)
                    if referenced_obj:
                        new_obj._referenced_objects[property_uri].append(referenced_obj)
                    else:
                        new_obj._referenced_objects[property_uri].append(SBOLObject(o.identity))
        else:
            # If the copy does not belong to a Document, then treat all references
            # like external references
            for property_uri, object_store in self._referenced_objects.items():
                for o in object_store:
                    new_obj._referenced_objects[property_uri].append(SBOLObject(o.identity))

        return new_obj

    def lookup(self):
        return self


def replace_namespace(old_uri, target_namespace, rdf_type):

    # Flag as not working to ensure nobody calls this function thinking
    # it might do something.
    # See https://github.com/SynBioDex/pySBOL3/issues/132
    raise NotImplementedError()


def make_resolve_references_traverser(new_obj) -> Callable:
    # Return a callback for traversing documents and updating
    # any references to new_obj

    def resolve_references(x):
        for property_id, references in x._referenced_objects.items():
            needs_updating = False
            for ref_obj in references:
                if ref_obj.identity == new_obj.identity:
                    needs_updating = True
                    break
            if needs_updating:
                references.remove(ref_obj)
                references.append(new_obj)

    return resolve_references
 

# Global store for builder methods. Custom SBOL classes
# register their builders in this store
BUILDER_REGISTER: Dict[str, Callable[[str, str], SBOLObject]] = {}
