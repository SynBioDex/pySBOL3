import posixpath
import uuid
from collections import defaultdict
from typing import Optional
from urllib.parse import urlparse
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

    def _validate_identity(self) -> None:
        # TODO: identity must be a URI
        # TODO: can identity be None?
        pass

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
        if base_uri.endswith('#'):
            return base_uri + name
        else:
            return posixpath.join(base_uri, name.lstrip(posixpath.sep))

    def validate(self) -> None:
        self._validate_identity()

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

        # new_obj = self.__class__(name=new_uri, type_uri=self.type_uri)
        new_obj = sbol3.Document._uri_type_map[type_uri](name=new_uri, type_uri=self.type_uri)

        # Copy properties
        for property_uri, value_store in self._properties.items():
            new_obj._properties[property_uri] = value_store.copy()

            # # Add a non-default namespace to the target document if not present
            # # (This can happen when copying extension properties not in the
            # # SBOL namespace, for example.)
            # if self.doc and target_doc is not None:
            #     property_namespace = URIRef(parseNamespace(property_uri))
            #     if property_namespace in namespace_map.keys():
            #         prefix = namespace_map[property_namespace]
            #         target_doc.addNamespace(property_namespace, prefix)

        # # If caller specified a target_namespace argument, then import objects into this
        # # new namespace. This involves replacing the target_namespace in ReferenceObject
        # # URIs with the current Homespace. Don't overwrite namespaces for the
        # # wasDerivedFrom field, which points back to the original object
        # if target_namespace:

        #     # Map the identity of self into the target namespace
        #     if hasattr(self, 'identity'):
        #         old_uri = self.identity
        #         new_uri = replace_namespace(old_uri, target_namespace, self.getTypeURI())
        #         new_obj.identity = new_uri

        #     if hasattr(self, 'persistentIdentity'):
        #         old_uri = self.persistentIdentity
        #         new_uri = replace_namespace(old_uri, target_namespace, self.getTypeURI())
        #         new_obj.persistentIdentity = new_uri

        #     # Map any references to other SBOL objects in the Document into the new
        #     # namespace
        #     if self.doc is not None:

        #         # Collect ReferencedObject attributes
        #         reference_properties = [p for p in new_obj.__dict__.values() if
        #                                 isinstance(p, ReferencedObject)]

        #         for reference_property in reference_properties:
        #             values = new_obj.properties[reference_property._rdf_type]
        #             new_values = []
        #             for uri in values:
        #                 if target_namespace in uri:

        #                     referenced_object = self.doc.find(uri)
        #                     if referenced_object is None:
        #                         continue
        #                     new_uri = replace_namespace(uri, target_namespace,
        #                                                 referenced_object.getTypeURI())
        #                     new_values.append(new_uri)
        #             new_obj.properties[reference_property._rdf_type] = new_values


        # Assign the new object to the target Document
        if target_doc:
            target_doc.add(new_obj)


        # When an object is simply being cloned, the value of wasDerivedFrom should be
        # copied exactly as is from self. However, when copy is being used to generate
        # a new entity, the wasDerivedFrom should point back to self.
        if self.identity == new_obj.identity:
            new_obj.derived_from = self.derived_from
        else:
            new_obj.derived_from = self.identity

        # # Copy child objects recursively
        # for property_uri, object_list in self.owned_objects.items():
        #     # Don't copy hidden properties
        #     if target_doc and property_uri in self._hidden_properties:
        #         continue
        #     for o in object_list:
        #         o_copy = o.copy(target_doc, target_namespace, version)
        #         new_obj.owned_objects[property_uri].append(o_copy)
        #         o_copy.parent = self
        #         # o_copy.update_uri()

        return new_obj


def replace_namespace(old_uri, target_namespace, rdf_type):
    """
    Utility function for mapping an SBOL object's identity into a new namespace. The
    rdf_type is used to map to and from sbol-typed namespaces.
    """

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
