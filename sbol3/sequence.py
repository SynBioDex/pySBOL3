from . import *


class Sequence(TopLevel):

    def __init__(self, identity: str, *, type_uri: str = SBOL_SEQUENCE) -> None:
        super().__init__(identity, type_uri)
        self.elements = TextProperty(self, SBOL_ELEMENTS, 0, 1)
        self.encoding = URIProperty(self, SBOL_ENCODING, 0, 1)
        self.validate()

    def validate(self) -> None:
        super().validate()
        # If sequence is set, encoding is REQUIRED
        if self.elements and not self.encoding:
            raise ValidationError('Sequence encoding is required if elements are set')


Document.register_builder(SBOL_SEQUENCE, Sequence)
