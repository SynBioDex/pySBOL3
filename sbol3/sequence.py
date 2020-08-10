from . import *


class Sequence(TopLevel):

    def __init__(self) -> None:
        super().__init__()
        self.elements = TextProperty(self, SBOL_ELEMENTS, 0, 1)
        self.encoding = URIProperty(self, SBOL_ENCODING, 1, 1)

    def validate(self) -> None:
        super().validate()
