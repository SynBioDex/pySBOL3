import math

from . import *


class TopLevel(Identified):

    def __init__(self, name: str, type_uri: str) -> None:
        super().__init__(name, type_uri)
        self.attachments = ReferencedObject(self, SBOL_HAS_ATTACHMENT, 0, math.inf)

    def validate_identity(self) -> None:
        # TODO: See section 5.1 for rules about identity for TopLevel
        super().validate_identity()

    def validate(self) -> None:
        super().validate()
