import math

from . import *


class TopLevel(Identified):

    def __init__(self, identity: str, type_uri: str) -> None:
        # Sanity check identity, which is required for a TopLevel
        # More checking on identity happens in Identified, but Identified
        # does not require an identity, only TopLevel does.
        if not identity or not isinstance(identity, str):
            raise ValueError('Identity must be a non-empty string')
        super().__init__(identity, type_uri)
        self.attachments = ReferencedObject(self, SBOL_HAS_ATTACHMENT, 0, math.inf)

    def validate_identity(self) -> None:
        # TODO: See section 5.1 for rules about identity for TopLevel
        super().validate_identity()

    def validate(self) -> None:
        super().validate()
