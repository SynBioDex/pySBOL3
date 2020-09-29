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
