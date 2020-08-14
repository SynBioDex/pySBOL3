import math
from urllib.parse import urlparse

from . import *


class Identified(SBOLObject):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._display_id = TextProperty(self, SBOL_DISPLAY_ID, 0, 1)
        self.name = TextProperty(self, SBOL_NAME, 0, 1)
        self.description = TextProperty(self, SBOL_DESCRIPTION, 0, 1)
        self.derived_from = URIProperty(self, PROV_DERIVED_FROM, 0, math.inf)
        self.generated_by = URIProperty(self, PROV_GENERATED_BY, 0, math.inf)
        # Identity has been set by the SBOLObject constructor
        self._display_id = Identified._extract_display_id(self.identity)

    @staticmethod
    def _is_valid_display_id(display_id: str) -> bool:
        # A display id [...] value MUST be composed of only alphanumeric
        # or underscore characters and MUST NOT begin with a digit.
        # (Section 6.1)
        #
        # Make sure everything other than underscores are alphanumeric, and
        # make sure the first character is not a digit.
        #
        # Note: This implies that '_' is not a valid displayId because `isalnum()`
        # will return false if the string is empty, which it will be after we filter
        # out the lone underscore.
        return display_id.replace('_', '').isalnum() and not display_id[0].isdigit()

    @staticmethod
    def _extract_display_id(identity: str) -> str:
        parsed = urlparse(identity)
        if not (parsed.scheme and parsed.netloc and parsed.path):
            raise ValueError(f'Expected URL, found {identity}')
        display_id = parsed.path.split('/')[-1]
        if Identified._is_valid_display_id(display_id):
            return display_id
        else:
            msg = f'"{display_id}" is not a valid displayId.'
            msg += '  A displayId MUST be composed of only alphanumeric'
            msg += ' or underscore characters and MUST NOT begin with a digit.'
            raise ValueError(msg)

    def _validate_display_id(self) -> None:
        # TODO: if identity is a URL, display_id is required
        if (Identified._is_valid_display_id(self.display_id) and
                self.identity.endswith(self.display_id)):
            return
        raise ValidationError(f'{self.display_id} is not a valid displayId')

    @property
    def display_id(self):
        # display_id is a read only property
        return self._display_id

    def validate(self) -> None:
        super().validate()
        self._validate_display_id()
