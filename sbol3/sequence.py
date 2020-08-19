from . import *


class Sequence(TopLevel):

    def __init__(self, name: str, *, type_uri: str = SBOL_SEQUENCE) -> None:
        super().__init__(name, type_uri)
        self.elements = TextProperty(self, SBOL_ELEMENTS, 0, 1)
        self.encoding = URIProperty(self, SBOL_ENCODING, 1, 1)

    def validate(self) -> None:
        super().validate()
