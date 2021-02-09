import posixpath
import uuid
from collections import defaultdict
from urllib.parse import urlparse
from typing import Dict, Callable, Optional

from . import *


class SBOLObject:

    def __init__(self, name: str, type_uri: str) -> None:
        self._properties = defaultdict(list)
        self._owned_objects = defaultdict(list)
        # Does this need to be a property? It does not get serialized to the RDF file.
        # Could it be an attribute that gets composed on the fly? Keep it simple for
        # now, and change to a property in the future if needed.
        self._identity = SBOLObject._make_identity(name)
        self.document = None
        # This is the URI for this object's type, used for serialization
        self.type_uri = type_uri

    def __setattr__(self, name, value):
        try:
            self.__dict__[name].set(value)
        except AttributeError:
            # Attribute set does not exist
            object.__setattr__(self, name, value)
        except KeyError:
            # property name does not exist
            object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        # Call the default method
        result = object.__getattribute__(self, name)
        if hasattr(result, '_sbol_singleton'):
            result = result.get()
        return result

    @staticmethod
    def _is_url(name: str) -> bool:
        parsed = urlparse(name)
        return bool(parsed.scheme and parsed.netloc and parsed.path)

    @staticmethod
    def _make_identity(name: str) -> str:
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
            return str(identity_uuid)
        except ValueError:
            pass
        # Not a URL or a UUID, so append to the namespace
        base_uri = get_namespace()
        if base_uri is None:
            msg = 'No default namespace available.'
            msg += ' Use set_namespace() to set one.'
            raise NamespaceError(msg)
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

    def copy(self, target_doc=None, target_namespace=None):

        new_uri = self.identity

        # If caller specified a target_namespace argument, then copy the object into this
        # new namespace.
        if target_namespace:

            # Map the identity of self into the target namespace
            if hasattr(self, 'identity'):
                old_uri = self.identity
                new_uri = replace_namespace(old_uri, target_namespace, self.getTypeURI())

        new_obj = BUILDER_REGISTER[self.type_uri](identity=new_uri,
                                                  type_uri=self.type_uri)

        # Copy properties
        for property_uri, value_store in self._properties.items():
            new_obj._properties[property_uri] = value_store.copy()

            # TODO:
            # Map into new namespace

        # Assign the new object to the target Document
        if target_doc:
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

        return new_obj


def replace_namespace(old_uri, target_namespace, rdf_type):
    """
    Utility function for mapping an SBOL object's identity into a new namespace. The
    rdf_type is used to map to and from sbol-typed namespaces.
    """

    # Flag as not working to ensure nobody calls this function thinking
    # it might do something.
    # See https://github.com/SynBioDex/pySBOL3/issues/132
    raise NotImplementedError()

    # Work around an issue where the Document itself is being copied and
    # doesn't have its own URI, so old_uri is None. Return empty string
    # because the identity is not allowed to be None.
    if old_uri is None:
        return ''

    # If the value is an SBOL-typed URI, replace both the namespace and class name
    class_name = parseClassName(rdf_type)
    replacement_target = target_namespace + '/' + class_name

    # If not an sbol typed URI, then just replace the namespace
    if replacement_target not in old_uri:
        replacement_target = target_namespace

    if Config.getOption(ConfigOptions.SBOL_TYPED_URIS):
        # Map into a typed namespace
        replacement = getHomespace() + '/' + class_name
    else:
        # Map into a non-typed namespace
        replacement = getHomespace()

    new_uri = old_uri.replace(replacement_target, replacement)
    if type(old_uri) is URIRef:
        return URIRef(new_uri)
    return new_uri


# Global store for builder methods. Custom SBOL classes
# register their builders in this store
BUILDER_REGISTER: Dict[str, Callable[[str, str], SBOLObject]] = {}
