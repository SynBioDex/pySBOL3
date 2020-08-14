import posixpath
import uuid
from collections import defaultdict
from urllib.parse import urlparse

from . import *


class SBOLObject:

    def __init__(self, name: str) -> None:
        self.properties = defaultdict(list)
        self.owned_objects = defaultdict(list)
        # Does this need to be a property? It does not get serialized to the RDF file.
        # Could it be an attribute that gets composed on the fly? Keep it simple for
        # now, and change to a property in the future if needed.
        self._identity = SBOLObject._make_identity(name)
        self.document = None

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
    def _make_identity(name: str) -> str:
        """Make an identity from the given name.

        If the name is a URL, that can be the identity. Or perhaps it
        needs to start with the default URI prefix (i.e. homespace).

        If the name is not a URL, prefix it with the default URI prefix
        (homespace) and verify that the result is a valid URL.

        We do not support UUIDs, which are legal SBOL identifiers.
        """
        parsed = urlparse(name)
        name_is_url = bool(parsed.scheme and parsed.netloc and parsed.path)
        if name_is_url:
            return name.strip(posixpath.sep)
        try:
            # If it is a UUID, accept it as the identity
            identity_uuid = uuid.UUID(name)
            return str(identity_uuid)
        except ValueError:
            pass
        # Not a URL or a UUID, so append to the homespace
        base_uri = get_homespace()
        if base_uri.endswith('#'):
            return base_uri + name
        else:
            return posixpath.join(base_uri, name)

    def validate(self) -> None:
        self._validate_identity()

    @property
    def identity(self):
        # identity is a read-only property
        return self._identity
