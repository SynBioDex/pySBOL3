import math
from urllib.parse import urlparse

from . import *


class Identified(SBOLObject):

    def __init__(self) -> None:
        super().__init__()
        # Does this need to be a property? It does not get serialized to the RDF file.
        # Could it be an attribute that gets composed on the fly?
        self.identity = None
        self.display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
        self.name = TextProperty(self, SBOL_NAME, 0, 1)
        self.description = TextProperty(self, SBOL_DESCRIPTION, 0, 1)
        self.derived_from = URIProperty(self, PROV_DERIVED_FROM, 0, math.inf)
        self.generated_by = URIProperty(self, PROV_GENERATED_BY, 0, math.inf)

    def validate_identity(self) -> None:
        # TODO: identity must be a URI
        # TODO: can identity be None?
        pass

    def validate_display_id(self) -> None:
        # TODO: If there is a display id, the value MUST be composed of only
        # TODO:     alphanumeric or underscore 14 characters and MUST NOT
        # TODO:     begin with a digit. (Section 6.1)

        parsed = urlparse(self.identity)
        identity_is_url = bool(parsed.scheme and parsed.netloc and parsed.path)
        if identity_is_url:
            # If the identity is a URL, the displayId MUST be set
            if not self.display_id:
                my_type = type(self).__name__
                msg = f'{my_type} {self.identity} does not have a display_id (Section 6.1)'
                raise ValidationError(msg)

    def validate(self) -> None:
        self.validate_identity()
        self.validate_display_id()
